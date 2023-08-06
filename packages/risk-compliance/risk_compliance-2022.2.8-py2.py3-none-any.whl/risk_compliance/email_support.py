#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 2021/12/15 14:15
@author: yuwenbin
"""
import smtplib
import sys
import time
import datetime
import requests
import json
import socket
import consul
import re
import logging
import threading
import os
import configparser
import xlsxwriter
import xlwt

from typing import Iterable, List, Optional
from abc import ABC, abstractmethod
from typing import List, Optional
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .data_support import Helper
from .data_support import Config



import warnings

warnings.simplefilter("ignore", ResourceWarning)


class Logger(object):
    _instance_lock = threading.Lock()
    level_relations = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}
    format_str = '%(asctime)s - %(name)s - %(module)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s'

    def __init__(self, name=None, lever='info', fmt=format_str, **kwargs):
        if not name:
            name = __name__
        self.name = name
        self.lever = self.level_relations.get(lever.lower(), logging.INFO)
        self.format_str = fmt
        self.logger = logging.getLogger(self.name)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with Logger._instance_lock:
                if not hasattr(cls, '_instance'):
                    Logger._instance = super().__new__(cls)
            return Logger._instance

    @property
    def get_logger(self):
        self.logger.setLevel(level=self.lever)
        formatter = logging.Formatter(self.format_str)
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        return self.logger

    def debug(self, message):
        """
        :param message: debug信息
        :return:
        """
        self.logger.debug(message)

    def info(self, message):
        """
        :param message: info信息
        :return:
        """
        self.logger.info(message)

    def warn(self, message):
        """
        :param warn: warn 信息
        :return:
        """
        self.logger.warn(message)

    def critical(self, message):
        """
        :param message: critical 信息
        :return:
        """
        self.logger.critical(message)

    def error(self, message):
        """
        :param message: error 信息
        :return:
        """
        self.logger.error(message)


class InvalidEmailAddress(Exception):
    """
    Note that this will only filter out syntax mistakes in emailaddresses.
    """
    pass


class InvalidAddress(Exception):
    """
    Note that this will only filter out syntax mistakes in addresses.
    """
    pass


class InvalidArguments(Exception):
    """
    Note that this will only filter out syntax mistakes in Arguments
    """
    pass


def make_list(obj) -> list:
    return obj if isinstance(obj, list) else [obj]


def get_abs_path(file: str) -> str:
    """if the file exists, return its abspath or raise a exception."""
    if os.path.exists(file):
        return file
    return False


# 获取文件大小
def get_doc_size(path):
    """if the file exists, return its size or raise a exception."""
    if os.path.exists(path):
        size = os.path.getsize(path)
        return int(size)
    raise InvalidAddress(f'{path} get size error ')


def make_attachment_part(file_path) -> MIMEBase:
    """According to file-type return a prepared attachment part."""
    name = os.path.split(file_path)[1]
    encoded_name = Header(name).encode()
    size = get_doc_size(file_path)
    file_type = 'application/octet-stream'
    main_type, sub_type = file_type.split('/')
    with open(file_path, 'rb') as f:
        part = MIMEBase(main_type, sub_type)
        part.set_payload(f.read())
        part['Content-Disposition'] = 'attachment;filename="{}"'.format(encoded_name)
        encode_base64(part)
    return part, int(size)


def validate_email_with_regex(email_address, regexp):
    """ with regexp check email address validity, return bool or raise a exception."""
    if re.match(r'{}'.format(regexp), email_address):
        return True
    else:
        raise InvalidEmailAddress('Emailaddress "{}" is Invalid email'.format(email_address))


def bool_check_func(v):
    if v.lower() == 'false':
        v = False
    elif v.lower() == 'true':
        v = True
    elif v.lower() == 'none':
        v = None
    return v


def check_limit_hsql(hql, sql_limit_size):
    """Check HQL limit """
    if re.search(r"limit.*?(\d+)", hql):
        num = re.search(r"limit.*?(\d+)", hql).group(1)
        if int(num) > int(sql_limit_size):
            hql = re.sub(r'limit.*?(\d+)', f'limit {sql_limit_size}', hql)
    else:
        hql = hql + f" limit {sql_limit_size}"
    return hql


def query_data(hql, sql_limit_size, url=None, message=None):
    """
    query hive sql and return result
    :param hql: hive sql
    :param url: request Reminder address
    :param message: Reminder message
    :return: query hql result
    """
    if not message:
        message = "query_data hive sql"
    hql = check_limit_hsql(hql, sql_limit_size)
    helper = Helper()
    result = helper.exec_hive(hql, message)
    return result


def make_hql_data_xlsx_to_file(hql_info, filrpath, title, sql_limit_size, url=None, stype='xlsx'):
    """
    query hql data and make excel file and return file path
    :param hql_info: [{hql:1 ----str,columns: 1----str,sheet_name:sheetName }]
    :param filrpath: file path default './python_email_data'
    :param url: request Reminder address
    :param title:  file title
    :param stype: 'xls' or 'xlsx'
    :return:
    """
    if stype not in ('xls', 'xlsx'):
        raise InvalidArguments('params type do not meatch')
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = str(title) + str(date_time) + '.' + 'xls'
    file_path = os.path.join(filrpath, filename)
    hql_list = make_list(hql_info)
    is_not_empty = 0
    work_book = xlsxwriter.Workbook(file_path)
    for msg_dict in hql_list:
        hql = msg_dict.get('hql', None)
        columns = msg_dict.get('columns', None)
        sheet_name = msg_dict.get('sheet_name', None)
        data = msg_dict.get('data', None)
        if not data:
            if hql and columns and sheet_name:
                data = query_data(hql, sql_limit_size=sql_limit_size, url=url)
        if not data:
            continue
        worksheet = work_book.add_worksheet(sheet_name)
        if not isinstance(columns, str):
            raise InvalidArguments('hql_info columns must be str')
        column_list = columns.split(',')
        worksheet.write_row(0, 0, column_list)
        for ix, row in enumerate(data):
            worksheet.write_row(ix + 1, 0, row)
        is_not_empty += 1
    work_book.close()
    if get_abs_path(file_path) and not is_not_empty:
        os.remove(file_path)
    return file_path, is_not_empty


def make_hql_data_xlwt_to_file(hql_info, filrpath, title, sql_limit_size, url=None, stype='xls', encoding='utf-8'):
    """
    query hql data and make excel file and return file path
    :param hql_info: [{hql:1 ----str,columns: 1----str,sheet_name:sheetName }]
    :param filrpath: file path default './python_email_data'
    :param url: request Reminder address
    :param title:  file title
    :param stype: 'xls' or 'xlsx' default 'xls'
    :param encoding: default 'utf-8'
    :return:
    """
    if stype not in ('xls', 'xlsx'):
        raise InvalidArguments('params type do not meatch')
    date_time = datetime.datetime.today().strftime('%Y-%m-%d')
    filename = str(title) + str(date_time) + '.' + str(stype)
    file_path = os.path.join(filrpath, filename)
    is_not_empty = 0
    hql_list = make_list(hql_info)
    work_book = xlwt.Workbook(encoding=encoding, style_compression=0)
    for msg_dict in hql_list:
        hql = msg_dict.get('hql', None)
        columns = msg_dict.get('columns', None)
        sheet_name = msg_dict.get('sheet_name', None)
        data = msg_dict.get('data', None)
        if not data:
            if hql and columns and sheet_name:
                data = query_data(hql, sql_limit_size=sql_limit_size, url=url)
        if not data:
            continue
        worksheet = work_book.add_sheet(sheet_name, cell_overwrite_ok=True)
        if not isinstance(columns, str):
            raise InvalidArguments('hql_info columns must be str')
        column_list = columns.split(',')
        for ix, field in enumerate(column_list):
            worksheet.write(0, ix, field)
        for ix, row in enumerate(data):
            for iy, v in enumerate(row):
                worksheet.write(ix + 1, iy, v)
        is_not_empty += 1
    if not is_not_empty:
        worksheet = work_book.add_sheet('sheetName_1', cell_overwrite_ok=True)
        worksheet.write(0, 0, 0)
        work_book.save(file_path)
        if get_abs_path(file_path):
            os.remove(file_path)
    else:
        work_book.save(file_path)
    return file_path, is_not_empty


def make_email_table_to_html(hql_info, maxRows, sql_limit_size, url=None):
    """
    query hql data and make html and return html str
    :param hql_info: [{hql:1 ----str,columns: 1----str,sheet_name:sheetName }]
    :param url: request Reminder address
    :param maxRows: table max Rows
    :return: html str
       """
    row_num = 0
    is_not_empty = 0
    hql_list = make_list(hql_info)
    table_html = "<html><head></head><body>"
    for msg_dict in hql_list:
        hql = msg_dict.get('hql', None)
        columns = msg_dict.get('columns', None)
        sheet_name = msg_dict.get('sheet_name', None)
        data = msg_dict.get('data', None)
        if not data:
            if hql and columns and sheet_name:
                data = query_data(hql, sql_limit_size=sql_limit_size, url=url)
        if not data:
            continue
        table_html += "<h2>" + sheet_name + "</h2>"
        if data and columns and sheet_name:
            th = "<table border=\"5\" style=\"border:solid 1px #E8F2F9;font-size=14px;;font-size:18px;\">"
            th += "<tr style=\"background-color: #428BCA; color:#ffffff\">"
            if not isinstance(columns, str):
                raise InvalidArguments('hql_info columns must be str')
            column_list = columns.split(',')
            for column in column_list:
                th += "<th>" + column + "</th>"
            th = th + "</tr>"
            tr = ""
            for row in data:
                td = ''
                row_num += 1
                if row_num > int(maxRows):
                    break
                for v in row:
                    td = td + "<td>" + str(v) + "</td>"
                tr = tr + "<tr>" + td + "</tr>"
            body = str(tr)
            tail = '</table>'
            table_html += th + body + tail
            is_not_empty += 1
    table_html += "<html><head></head><body>"
    return table_html, is_not_empty


class ConsulClient(object):
    _consul = None

    def __init__(self, host: str, port: int, token: str = None):
        self.host = host
        self.port = port
        self.token = token
        self._consul = consul.Consul(host, port, token=token)

    def register(self, service_name, address, port, schema='tcp'):
        if schema.lower() == 'tcp':
            check = consul.Check.tcp(address, port, "10s")  #
        else:
            check = consul.Check.http(f'{schema}:{address}:{port}/actuator/health', "1s",
                                      "3s", "10s")

        service_id = f"{service_name}-{address}-{port}"
        self._consul.agent.service.register(service_name, service_id=service_id, address=address, port=port,
                                            check=check)

    def deregister(self, service_name, address, port):
        service_id = f"{service_name}-{address}-{port}"
        self._consul.agent.service.deregister(service_id)

    def get_services(self) -> list:
        return self._consul.catalog.services()[1].keys()

    def get_consul_kv(self, config_path, *args):
        """
        :param c: consul instance
        :param config_path: consul config path
        :param args: consul keys to be obtained
        :return: list of str value

        Examples:
        config_path = 'config/example
        c_keys = ['sql_host','sql_user','sql_db']
        c_values = load_consul(c,config_path,*c_keys)
        or:
        c_values = load_consul(c,config_path,'sql_host','sql_user','sql_db')
        or:
        sql_host,sql_user,sql_db = load_consul(c,config_path,*c_keys)

        Note: float or int value need to be converted later
        server_port = load_consul(c, config_path, 'server_port')
        server_port = int(server_port)
        """
        args_value = []
        if not args:
            raise ValueError('Empty input consul arguments, should be a list')
        for arg in args:
            c_key = config_path + '/{}'.format(arg)
            _, c_value = self._consul.kv.get(c_key)
            if c_value:
                value = str(c_value['Value'], encoding='utf8')
                args_value.append(value)
            else:
                print('Warning: key: {} does not exist in {}'.format(arg, config_path))

        if len(args_value) == 1:
            args_value = args_value[0]

        return args_value

    def get_vault_kv(self, server_name, vault_token,vault_version=None, *args):
        """链接consul 获取vault服务，获取vault服务参数，请求vault服务，根据k值获取对应的v值"""
        if not args:
            raise ValueError('Empty input consul arguments, should be a list')
        vault = self._consul.catalog.service('vault')
        vault_ip = vault[1][0]['ServiceAddress']
        vault_port = vault[1][0]['ServicePort']
        if vault_version:
            vault_url = f"http://{vault_ip}:{vault_port}/v{vault_version}/secret/{server_name}"
        else:
            vault_url = 'http://{}:{}/v1/secret/{}'.format(vault_ip, vault_port, server_name)
        vault_headers = {'X-Vault-Token': vault_token}
        req = requests.get(url=vault_url, headers=vault_headers)
        args_value = []
        if req.status_code == 200:
            req = json.loads(req.text)
            if 'data' in req:
                data = req['data']
                for arg in args:
                    if arg in data:
                        args_value.append(data[arg])
                    else:
                        print('key: {} not in valut'.format(arg))
            else:
                raise IndexError
        else:
            raise RuntimeError('valut connection failed, reason: {} {}'.format(req.reason, req.text))

        if len(args_value) == 1:
            args_value = args_value[0]

        return args_value


def get_host_ip():
    """获取本地ip"""
    ip = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


class Mail:
    """
    mail 类 组装mail MIMEMultipart ,
    mail --dict {To、From、Cc、Subject、title、content_html、content_text、 hql_info、sendByAnnex、maxRows、isSendFlag等}
    cnf 为配置类; log 为日志类
    return 邮件体 mine
    """

    def __init__(self, mail: dict, cnf: object = None,
                 log: logging.Logger = None):
        if isinstance(cnf, object):
            self.cnf = cnf
        else:
            raise InvalidArguments('cnf field excepted type object got {}'.format(type(mail)))
        if isinstance(mail, dict):
            self.mail = mail
        else:
            raise InvalidArguments('mail field excepted type dict got {}'.format(type(mail)))
        self.log = log
        self.send_by_annex = int(self.mail.get('sendByAnnex', 1))
        self.isSendFlag = int(self.mail.get('isSendFlag', 0))
        if int(self.send_by_annex) == 1:
            self.multipart = 'mixed'
        else:
            self.multipart = 'alternative'
        if not self.mail.get('title'):
            raise InvalidArguments('mail field excepted title ')
        self.title = self.mail.get('title')
        self.mail_annex_max_size = int(self.mail.get('mail_annex_max_size'))
        self.mail_content_max_size = int(self.mail.get('mail_content_max_size'))
        self.maxRows = int(self.mail.get('mail_table_max_row', 500))
        if self.mail.get('lang'):
            self.lang = self.mail.get('lang')
        else:
            self.lang = self.cnf.get_value('smtp_mail', 'lang')
        try:
            self.encoding = self.cnf.get_value('smtp_mail', 'encoding')
        except:
            self.encoding = 'utf-8'
        self.mime = None  # type:MIMEMultipart

    def get_subject(self, lang=None):
        """
        获取邮件主题
        :param lang: 语言
        :return: 主题 str
        """
        date_time = datetime.datetime.today().strftime('%Y-%m-%d')
        subject = self.mail.get('subject')
        if not subject:
            if lang == 'zh':
                subject = "【后台数据导出】" + self.title + "-" + date_time
            else:
                subject = self.title + " - " + date_time
        subject = subject + " (" + datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y") + ")"
        return subject

    def get_content(self, mime, lang=None):
        """
        构造邮件正文
        :param mime: 邮件体
        :param lang: 语言
        :return: 邮件体 mime  ，正文大小 size
        """
        # Set extra headers.
        size = 0
        if self.mail.get('content_html') or self.mail.get('content_text'):
            # Set HTML content.
            content_html = self.mail.get('content_html')
            if content_html is not None:
                _htmls = make_list(content_html)
                for _html in _htmls:
                    mime.attach(MIMEText('{}'.format(_html), 'html', 'utf-8'))
                    size += len(_html)
            # Set TEXT content.
            if self.mail.get('content_text') is not None:
                _messages = make_list(self.mail['content_text'])
                for _message in _messages:
                    size += len(_message)
                    mime.attach(MIMEText('{}'.format(_message), 'plain', 'utf-8'))
        else:
            if lang == 'zh':
                content = "Hi All: <br>      附件是今天的" + self.title + "，请查收。"
            else:
                content = "Hi All: <br>      Please check today's " + str(self.title).lower()
            content = content + '<br><br>'
            size += len(content)
            mime.attach(MIMEText('{}'.format(content), 'html', 'utf-8'))
        return mime, size

    def get_attachments(self, mime):
        """
        获取附件
        :param mime: 邮件体 mime
        :return:
        """
        sumsize = 0
        if self.mail.get('attachments'):
            attachments = make_list(self.mail['attachments'])
            for attachment in attachments:
                if isinstance(attachment, str):
                    attachment_abs_path = get_abs_path(attachment)
                    part, size = make_attachment_part(attachment_abs_path)
                    sumsize += size
                    mime.attach(part)
                    os.remove(attachment)
                elif isinstance(attachment, tuple):
                    name, raw = attachment
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(raw)
                    part['Content-Disposition'] = 'attachment;filename="{}"'.format(name)
                    encode_base64(part)
                    mime.attach(part)
                else:
                    self.log.error(
                        '{} access error:{}'.format(self.__class__.__name__, 'Attachments except str or tuple'),
                        exc_info=True)
                    raise InvalidArguments('Attachments excepted str or tuple got {} instead.'.format(type(attachment)))
        return mime, sumsize

    def make_mine(self) -> None:
        """构造邮件体"""
        self.log.info('make_mine begin')
        mime = MIMEMultipart(self.multipart)
        subject = self.get_subject(lang=self.lang)
        if self.lang == 'zh':
            mime["Accept-Language"] = "zh-CN"
        mime['From'] = self.mail.get('From')
        mime['To'] = self.mail.get('To')
        if self.mail.get('Cc'):
            mime['Cc'] = self.mail.get('Cc')
        if self.mail.get('Bcc'):
            mime['Bcc'] = self.mail.get('Bcc')
        mime['Subject'] = subject
        mime["Accept-Charset"] = "ISO-8859-1,{}".format(self.encoding)
        # Set extra headers.
        if self.mail.get('headers') and isinstance(self.mail['headers'], dict):
            for k, v in self.mail['headers'].items():
                mime[k] = v
        # Set attachments.
        content_size = 0
        table_mail = self.mail.get('table_mail', '')
        content_html = ''
        if self.send_by_annex == 0 and table_mail:
            content_html += self.mail.get('content_html', '')
            content_html += table_mail
            content_size += len(content_html)
            mime.attach(MIMEText('{}'.format(content_html), 'html', 'utf-8'))
        else:
            mime, con_size = self.get_content(mime, lang=self.lang)
            content_size += con_size
            if int(self.mail.get('sendByAnnex')) == 1:
                mime, sumsize = self.get_attachments(mime)
                if not self.isSendFlag and not sumsize:
                    self.log.error('{} access error :{}'.format(self.__class__.__name__,
                                                                'sendByAnnex = 1 and isSendFlag = 0 and content empty'),
                                   exc_info=True)
                    raise InvalidArguments('sendByAnnex = 1 and isSendFlag = 0 and content empty')
                if sumsize > int(self.mail_annex_max_size):
                    self.log.error(
                        '{} access error :{}'.format(self.__class__.__name__, 'mail annex size Over limit'),
                        exc_info=True)
                    raise InvalidArguments('mail size Over limit')
        if content_size > int(self.mail_content_max_size):
            self.log.error('{} access error :{}'.format(self.__class__.__name__, 'mail_content Over limit'),
                           exc_info=True)
            raise InvalidArguments('content Over limit')
        if content_size == 0 and self.isSendFlag == 0:
            self.log.error('{} access error :{}'.format(self.__class__.__name__, 'mail_content is empty'),
                           exc_info=True)
            raise InvalidArguments('isSendFlag == 0 and content empty')
        self.log.debug('make mime finish')
        self.mime = mime

    def set_mime_header(self, k, v) -> None:
        if self.mime is not None:
            self.mime[k] = v
        else:
            self.make_mine()
            self.mime[k] = v

    def get_mime_raw(self) -> MIMEMultipart:
        if self.mime is not None:
            return self.mime
        else:
            self.make_mine()
            return self.mime

    def get_mime_as_string(self) -> str:
        return self.get_mime_raw().as_string()

    def get_mime_as_bytes_list(self) -> List[bytes]:
        return self.get_mime_as_string().encode('utf-8').split(b'\n')

    def _is_resend_mail(self) -> bool:
        return all([(i in self.mail) for i in
                    ('from', 'to', 'subject', 'raw_headers', 'charsets', 'headers',
                     'date', 'id', 'raw', 'attachments', 'content_text', 'content_html')])


class BaseServer(ABC):
    """Base protocol server."""

    def __init__(self, username: str, password: str,
                 host: str, port: int,
                 ssl: bool, tls: bool,
                 timeout: int or float,
                 debug: bool, log: Optional[logging.Logger] = None):
        self.server = None
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout
        self.ssl = ssl
        self.tls = tls
        self.debug = debug
        self.log = log
        self._login = False

        if tls and ssl:
            raise TypeError('Can not use ssl and tls together.')

    @abstractmethod
    def _make_server(self):
        pass

    def _remove_server(self):
        self.server = None

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def logout(self):
        pass

    @abstractmethod
    def stls(self):
        pass

    def check_available(self) -> bool:
        try:
            self.login()
            self.logout()
            return True
        except Exception as e:
            self.log.error('{} access error :{}'.format(self.__class__.__name__, e), exc_info=True)
            return False

    def is_login(self) -> bool:
        return self._login

    def log_exception(self, msg):
        self.log.fatal(msg)

    def log_access(self, msg):
        self.log.debug('<{} {}:{} ssl:{} tls:{} is_login:{}> {}.'
                       .format(self.__class__.__name__,
                               self.host, self.port,
                               self.ssl, self.tls,
                               self.is_login(), msg))

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def __repr__(self):
        return '<{} username:{} password:{} ' \
               '{}:{} ssl:{} tls:{}>' \
            .format(self.__class__.__name__, self.username, self.password,
                    self.host, self.port, self.ssl, self.tls)


class SMTPServer(BaseServer):
    """Base SMTPServer, which encapsulates python3 standard library to a SMTPServer."""

    def _make_server(self):
        """Init Server if possible."""

        if self.server is None:
            if self.ssl:
                self.server = smtplib.SMTP_SSL(self.host, self.port)
            else:
                self.server = smtplib.SMTP(self.host, self.port)

    def _remove_server(self):
        self.server = None

    def login(self):
        if self._login:
            self.log_exception('{} duplicate login!'.format(self.__repr__()))
            return
        self._make_server()
        if self.tls:
            self.stls()
        self.server.login(self.username, self.password)
        self._login = True

    def logout(self):
        if not self._login:
            self.log_exception('{} Logout before login!'.format(self.__repr__()))
            return
        try:
            code, message = self.server.docmd("QUIT")
            if code != 221:
                raise smtplib.SMTPResponseException(code, message)
        except smtplib.SMTPServerDisconnected:
            pass
        finally:
            self.server.close()
        self._remove_server()
        self._login = False

    def stls(self):
        """Start TLS."""
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

    # Methods
    def send(self, recipients: Iterable[str], mail: Mail,
             timeout: int or float or None):
        if timeout is not None:
            self.server.timeout = timeout
        self.server.sendmail(self.username, recipients, mail.get_mime_as_string())


class EmailServer:
    """email服务类"""

    def __init__(self, user, password, host, port, cnf: object = None, debug: bool = False, log=None, timeout=60):
        self.configer = cnf
        self.smtp_ssl = bool_check_func(self.configer.get_value('smtp_mail', 'ssl'))
        self.smtp_tls = bool_check_func(self.configer.get_value('smtp_mail', 'tls'))
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.log = log
        self.debug = debug
        self.timeout = timeout

        # Check arguments.
        if not isinstance(self.log, object):
            raise InvalidArguments('log excepted type object got {}'.format(type(self.log)))

        if not isinstance(self.timeout, (int, float)):
            raise InvalidArguments('timeout excepted type int or float got {}'.format(type(self.timeout)))
        self.smtp_server = SMTPServer(username=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      ssl=self.smtp_ssl,
                                      tls=self.smtp_tls,
                                      timeout=self.timeout,
                                      debug=self.debug,
                                      log=self.log
                                      )

    def send_mail(self, recipients: str, mail: dict, timeout=None) -> bool:
        """"Send email."""
        _mail = Mail(mail=mail, cnf=self.configer, log=self.log)
        if not timeout:
            timeout = self.timeout
        with self.smtp_server as server:
            server.send(recipients, _mail, timeout)
            self.log.info('send mail over')
        return True


def send_email(mail_info, con_file=None):
    """
    发送邮件方法
    :param mail_info  {hql_info dict -- hql详情，字典形式，字段有hql、columns、sheet_name、data（支持直接传递 数据2元数组）、
    mailTos str --收件人、mailCcs str --抄送人、Subject str --邮件主题、title str --邮件标题、content_html str --邮件正文html格式
    、content_text --str 邮件正文 plain形式、sendByAnnex int --是否带附件标志、默认1 带附件 、
    isSendFlag int -- 空邮件是否发送标志 默认0 不发送}
    """
    result = 0
    if not isinstance(mail_info, dict):
        raise InvalidArguments('mail_info field excepted type dict got {}'.format(type(mail_info)))
    if con_file:
        cnf = Config(file=con_file)
    else:
        cnf = Config()
    logger = Logger().get_logger
    consul_port = cnf.get_value('smtp_mail', 'consul_port')
    server_name = cnf.get_value('smtp_mail', 'server_name')
    consul_host = os.getenv('spring.cloud.consul.host', '127.0.0.1')
    consul_token = os.getenv('spring.cloud.consul.config.acl-token')
    vault_token = os.getenv('spring_cloud_vault_token')
    # # 连接consul
    discover = ConsulClient(host=consul_host, port=consul_port, token=consul_token)
    config_path = 'config/{}'.format(server_name)
    c_keys = ['mail.service.host', 'mail.service.sender', 'mail.service.port',
              'mail.content.max.size', 'mail.annex.max.size', 'mail.table.max.row', 'vault.version',
              'mail.sql.limit.size']

    mail_host, mail_sender, mail_port, mail_content_max_size, mail_annex_max_size, mail_table_max_row, vault_version, sql_limit_size = discover.get_consul_kv(
        config_path,
        *c_keys)
    # 读取vault参数
    v_keys = ['mail.service.password']
    mail_password = discover.get_vault_kv(server_name, vault_token, vault_version, *v_keys)

    logger.debug('load over')
    if not mail_host or not mail_sender or not mail_password or not mail_content_max_size:
        raise InvalidArguments('missing mail configuration information for example mail_host')
    mail_info['From'] = mail_sender
    mail_info['mail_host'] = mail_host
    mail_info['mail_password'] = mail_password
    mail_info['mail_port'] = mail_port
    mail_info['mail_content_max_size'] = mail_content_max_size
    mail_info['mail_annex_max_size'] = mail_annex_max_size
    mail_info['mail_table_max_row'] = mail_table_max_row
    hql_info = mail_info.get('hql_info')
    reciver = list()
    Tos = mail_info.get('mailTos', None)
    Ccs = mail_info.get('mailCcs', None)
    if not Tos:
        raise Exception('missing mailTos')
    reciver = reciver + Tos.split(',')
    regexp = cnf.get_value('smtp_mail', 'valid_address_regexp')
    if Ccs:
        reciver = reciver + Ccs.split(',')
        mail_info['Cc'] = Ccs
    if reciver:
        for address in reciver:
            validate_email_with_regex(address, regexp)
    mail_info['To'] = Tos
    if int(mail_info.get('sendByAnnex')) == 1:
        title = mail_info.get('title', None)
        os_path = cnf.get_value('smtp_mail', 'file_path')
        if not os.path.exists(os_path):
            os.makedirs(os_path)
        filepath, is_not_empty = make_hql_data_xlwt_to_file(hql_info, os_path, title,
                                                            sql_limit_size=sql_limit_size)
        if is_not_empty:
            mail_info['attachments'] = filepath
    elif int(mail_info.get('sendByAnnex')) == 0:
        table_email, is_not_empty = make_email_table_to_html(hql_info, mail_table_max_row,
                                                             sql_limit_size=sql_limit_size)
        mail_info['table_mail'] = table_email
    if not is_not_empty and int(mail_info.get('isSendFlag', 0)) == 0:
        return result
    logger.info('begin EmailServer')
    email_sever = EmailServer(cnf=cnf, log=logger, user=mail_sender, password=mail_password, host=mail_host,
                              port=int(mail_port))
    result = email_sever.send_mail(recipients=reciver, mail=mail_info)
    logger.info('result:{}'.format(result))
    return result

# if __name__ == '__main__':
#     print()
#     logger = Logger()
#     logger.info("Start print log")
