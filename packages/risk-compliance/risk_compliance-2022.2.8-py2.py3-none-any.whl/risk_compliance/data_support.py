# -*- coding: utf-8 -*
from pyhive import hive
import requests
import json
import re
import sys
import datetime
import time
import calendar
import threading
import configparser
from dateutil import tz
import os
from .consul import ConsulClient

# 设置周一为一周第一天
calendar.setfirstweekday(firstweekday=6)

"""
基础函数
author chenhui
date 2021-11-08
"""


def run_hive(sql, host1, host2, port, username, message, url, users=None):
    try:
        sqls = '''set hive.tez.auto.reducer.parallelism=true;
        set hive.exec.reducers.max=99;
        set hive.merge.tezfiles=true;
        set hive.merge.smallfiles.avgsize=32000000;
        set hive.merge.size.per.task=128000000;
        set tez.queue.name=analyst;''' + sql
        sqllist = [j for j in sqls.strip().split(';') if j != '']
        res = []
        conn = hive.connect(host=host1, port=port, username=username)
        cursor = conn.cursor()
        for i in sqllist:
            start = time.time()
            cursor.execute(i)
            end = time.time()
            if end - start > 180:
                print('sql执行开始时间: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
                print(i)
                print('sql执行结束时间: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end)))
                print('sql执行总耗时大于3分钟: %s' % round(end - start, 2))
            try:
                res = cursor.fetchall()
            except:
                pass
            conn.commit()
        conn.close()
        return res
    except:
        try:
            conn = hive.connect(host=host2, port=port, username=username)
            cursor = conn.cursor()
            for i in sqllist:
                start = time.time()
                cursor.execute(i)
                end = time.time()
                if end - start > 180:
                    print('sql执行开始时间: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start)))
                    print(i)
                    print('sql执行结束时间: %s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end)))
                    print('sql执行总耗时大于3分钟: %s' % round(end - start, 2))
                try:
                    res = cursor.fetchall()
                except:
                    pass
                conn.commit()
            conn.close()
            return res
        except Exception as e:
            try:
                error = '告警消息: ' + message + '\n' + i + '\n' + re.match(r'.* (FAILED:.*)', str(e)).group(1)
            except:
                error = '告警消息: ' + i + '\n' + str(e)
            finally:
                headers = {'Content-Type': 'application/json'}
                if not users:
                    data = {
                        "msgtype": "text",
                        "text": {
                            "content": error,
                        }
                    }
                    response = requests.post(url, data=json.dumps(data), headers=headers)
                else:
                    config = Config()
                    alarm_host = config.get_config('alarm_host')
                    users_url = alarm_host + "?title=数据支撑告警&module=风控合规&users=" \
                                + users + "&mesg=" + error
                    html = requests.get(users_url, {}, headers=headers)

                raise Exception("hive opreation，error:{}".format(error))


def send_alert(message, url=None, users=None):
    config = Config()
    message = '提示消息: ' + str(message)
    headers = {'Content-Type': 'application/json'}
    if not users:
        data = {
            "msgtype": "text",
            "text": {
                "content": message,
            }
        }
        response = requests.post(config.get_config('alarm_url') if not url else url, data=json.dumps(data),
                                 headers=headers)
    else:
        alarm_host = config.get_config('alarm_host')
        users_url = alarm_host + "?title=数据支撑告警&module=风控合规&users=" \
                    + users + "&mesg=" + message
        html = requests.get(users_url, {}, headers=headers)


def us_time_conversion(sdatestr):
    """
    冬令时、夏令时判断，将北京时间转换为美东时间的东夏令时 # 夏令时（3月11日至11月7日），冬令时（11月8日至次年3月11日）
    :param sdatestr: 日期，str，如'1990-01-01'
    :return: sdatestr--当前日期-str,start_time--美东令时的当天开始时间-str,end_time--美东令时的当天结束时间-str
    """
    try:
        start_time = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyy，如：1990-01-01，error:{}".format(e))
    end_time = start_time + datetime.timedelta(days=1)
    sdatestr = start_time.strftime("%Y-%m-%d")
    start_mon = start_time.month
    start_day = start_time.day
    is_summer_day = 0
    if (start_mon > 3) and (start_mon < 11):
        is_summer_day = 1
    elif (start_mon == 3) and (start_day - 11 >= 0):
        is_summer_day = 1
    elif (start_mon == 11) and (start_day - 7 <= 0):
        is_summer_day = 1
    else:
        is_summer_day = 0
    if is_summer_day:
        start_time = start_time.strftime("%Y-%m-%d") + " 04:00:00"
        end_time = end_time.strftime("%Y-%m-%d") + " 04:00:00"
    else:
        start_time = start_time.strftime("%Y-%m-%d") + " 05:00:00"
        end_time = end_time.strftime("%Y-%m-%d") + " 05:00:00"

    return sdatestr, start_time, end_time


def get_first_last_day(year, month):
    """
    返回指定月份的第一天和最后一天
    :param year: 年份，int类型，如1990
    :param month: 月份，int类型，如1
    :return: firstDay-月初, lastDay-月末
    """
    try:
        datetime.datetime.strptime(str(year) + '0101', "%Y-%m-%d")
    except Exception as e:
        raise Exception("year 参数格式必须是yyyy，如：1990，error:{}".format(e))
    try:
        datetime.datetime.strptime('1990' + str(month) + '01', "%Y-%m-%d")
    except Exception as e:
        raise Exception("month 参数格式必须是yyyy，如：08，error:{}".format(e))
    # 获取当前月的第一天的星期和当月总天数
    weekDay, monthCountDay = calendar.monthrange(year, month)
    # 获取当前月份第一天
    firstDay = datetime.date(year, month, day=1)
    # 获取当前月份最后一天
    lastDay = datetime.date(year, month, day=monthCountDay)
    # 返回第一天和最后一天
    return firstDay.strftime("%Y-%m-%d"), lastDay.strftime("%Y-%m-%d")


def get_monday_firday(sdatestr):
    """
    返回星期一和星期五的日期
    :param sdatestr: 初始时间，如'1990-01-01'
    :return:  monday--周一,friday--周二
    """
    try:
        start_day = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyy，如：1990，error:{}".format(e))
    weekday = start_day.weekday()
    monday = start_day - datetime.timedelta(days=weekday)
    friday = monday + datetime.timedelta(days=4)
    return monday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d")


def date_compare(sdatestr, edatestr):
    """
    start,end两个时间比较，返回bool值
    :param start: 日期，字符串格式'2021-01-01'
    :param end: 日期，字符串格式'2021-01-02'
    :return: bool值 true 表示start>end
    """
    try:
        start = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
        end = datetime.datetime.strptime(edatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyy，如：1990-01-01，error:{}".format(e))
    return start > end


def get_month_early(sdatestr, n):
    """
    返回指定日期start前n个月的月初日期
    :param start: 开始日期 '1990-01-01'
    :param n: 前n个月 int类型，如3
    :return: 月初日期
    """
    try:
        sdate = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyy，如：1990-01-01，error:{}".format(e))
    month = sdate.month
    year = sdate.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1).strftime("%Y-%m-%d")


def get_date_by_times(sdatestr, edatestr):
    """
    根据开始日期、结束日期返回这段时间里所有天的集合
    :param sdatestr: 日期，字符串格式'2021-01-01'
    :param edatestr: 日期，字符串格式'2021-01-01'
    :return: 日期列表，list(str,)
    """
    try:
        datestart = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
        dateend = datetime.datetime.strptime(edatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyymmdd，如：1990-01-01，error:{}".format(e))
    daylist = []
    daylist.append(datestart.strftime("%Y-%m-%d"))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        daylist.append(datestart.strftime("%Y-%m-%d"))
    return daylist


def get_date_by_offset(sdatestr, before_day):
    """
     获取前1天或N天的日期，before_day=1：前1天；before_day=N：前N天
    :param sdatestr: 日期，str,如'2021-01-01'，开始日期
    :param before_day: 前before_day天，int，如5
    :return: re_date-日期，str,如'2021-01-01'，结束日期
    """
    try:
        datestart = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyymmdd，如：1990-01-01，error:{}".format(e))
    # 计算偏移量
    offset = datetime.timedelta(days=-before_day)
    # 获取想要的日期的时间
    re_date = (datestart + offset).strftime("%Y-%m-%d")
    return re_date


def caltime(sdatestr, edatestr):
    """
    计算两个日期相差天数，自定义函数名，和两个日期的变量名
    #根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
    #date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    :param sdatestr: 日期，str,如2021-01-01，开始日期
    :param edatestr: 日期，str,如2021-01-01，结束日期
    :return:
    """
    try:
        # "%Y-%m-%d %H:%M:%S"  计算日期还是日期时间
        datestart = datetime.datetime.strptime(sdatestr, "%Y-%m-%d")
        dateend = datetime.datetime.strptime(edatestr, "%Y-%m-%d")
    except Exception as e:
        raise Exception("参数格式必须是yyyymmdd，如：1990-01-01，error:{}".format(e))
    return (datestart - dateend).days


def get_hive_config(server_app_name, consul_post):
    consul_host = os.getenv('spring.cloud.consul.host', '127.0.0.1')
    consul_token = os.getenv('spring.cloud.consul.config.acl-token')

    consul_client = ConsulClient(host=consul_host, port=consul_post, token=consul_token)
    config_path = 'config/{}/'.format(server_app_name)

    _hive_info = {}

    c_keys = ['hive.host', 'backup.hive.host', 'alarm.host']
    hive_host, backup_hive_host, alarm_host = consul_client.get_consul_kv(config_path, *c_keys)
    _hive_info['hive.host'] = hive_host
    _hive_info['backup.hive.host'] = backup_hive_host
    _hive_info['alarm.host'] = alarm_host
    return _hive_info


"""
hive执行帮助类
author zhouyuqin
date 2021-11-23
"""


class Config(object):
    """
    配置类
    """
    _instance_lock = threading.Lock()
    # 属性字典，将配置信息放入属性中
    _attribute = {}

    def __init__(self, file="/deployments/hive.conf", *args, **kwargs):
        self.file = file

        self.conf = configparser.ConfigParser()
        self.conf.read(file)

        self._attribute['username'] = self.conf.get("hive", "username")
        self._attribute['port'] = self.conf.get("hive", "port")

        self._attribute['bucket'] = self.conf.get("s3", "bucket")
        self._attribute['path'] = self.conf.get("s3", "path")

        self._attribute['database'] = self.conf.get("db", "database")

        self._attribute['alarm_url'] = self.conf.get("alarm", "url")

        server_app_name = self.conf.get("server", "app_name")
        self._attribute['server_app_name'] = server_app_name

        consul_post = self.conf.get("consul", "port")
        self._attribute['consul_post'] = consul_post

        hive_config = get_hive_config(server_app_name, consul_post)
        self._attribute['host'] = hive_config['hive.host']
        self._attribute['backup_host'] = hive_config['backup.hive.host']
        self._attribute['alarm_host'] = hive_config['alarm.host']

    def __new__(cls, *args, **kwargs):
        """
        python类默认先调用__new__方法，这里重写__new__方法，让其能够判断是否已经存在对象，如果存在直接返回，如果不存在再去初始化
        :param args:参数
        :param kwargs:参数
        """
        if not hasattr(cls, '_instance'):
            with Config._instance_lock:
                if not hasattr(cls, '_instance'):
                    Config._instance = super().__new__(cls)
        return Config._instance

    def get_config(self, key):
        return self._attribute.get(key)

    def get_sections(self):
        """
        :return: 获取文件所有的sections
        """
        sections = self.conf.sections()
        return sections

    def get_options(self, section):
        """
        :param section: 获取某个section所对应的键
        :return:
        """
        options = self.conf.options(section)
        return options

    def get_items(self, sections):
        """
        :param sections: 获取某个section所对应的键值对
        :return:
        """
        items = self.conf.items(sections)
        return items

    def get_value(self, section, key):
        """
        :param sections:
        :param key:
        :return: 获取某个section某个key所对应的value
        """
        value = self.conf.get(section, key)
        return value


class Helper(object):
    # 创建中间表
    create_as_table = '''
    drop table if exists {database}.{table_name};
    create table if not exists {database}.{table_name}
    ROW FORMAT SERDE
    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES ('field.delim'='\\t','line.delim'='\\n','serialization.format'='\\t')
    STORED AS INPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
    's3n://{bucket}/data/{path}/{database}/{table_name}'
    TBLPROPERTIES ('last_modified_by'='hadoop','orc.compress'='SNAPPY')
    as
    {query_hql};'''

    # 创建分区表
    create_default_partition_table_and_insert = '''
    create table if not exists {database}.{table_name}(
    {column_info}
    )PARTITIONED BY (yyyymmdd string COMMENT '分区日期')
    ROW FORMAT SERDE
    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES
    ('field.delim'='\\t', 'line.delim'='\\n', 'serialization.format'='\\t')
    STORED AS INPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
    's3n://{bucket}/data/{path}/{database}/{table_name}'
    TBLPROPERTIES ('EXTERNAL'='FALSE','bucketing_version'='2','orc.compress'='SNAPPY');
    insert overwrite table {database}.{table_name}
    partition (yyyymmdd='{yyyymmdd}')
    {query_sql};'''

    # 创建分区表
    create_partition_table = '''
    create table if not exists {database}.{table_name}(
    {column_info}
    )PARTITIONED BY ({partition_info})
    ROW FORMAT SERDE
    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES
    ('field.delim'='\\t', 'line.delim'='\\n', 'serialization.format'='\\t')
    STORED AS INPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
    's3n://{bucket}/data/{path}/{database}/{table_name}'
    TBLPROPERTIES ('EXTERNAL'='FALSE','bucketing_version'='2','orc.compress'='SNAPPY');
    {insert_sql};'''

    # 创建分区表
    create_default_partition_table = '''
    create table if not exists {database}.{table_name}(
    {column_info}
    )PARTITIONED BY (yyyymmdd string COMMENT '分区日期')
    ROW FORMAT SERDE
    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES
    ('field.delim'='\\t', 'line.delim'='\\n', 'serialization.format'='\\t')
    STORED AS INPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
    's3n://{bucket}/data/{path}/{database}/{table_name}'
    TBLPROPERTIES ('EXTERNAL'='FALSE','bucketing_version'='2','orc.compress'='SNAPPY');
    {insert_sql};'''

    s3_location_info = '''ROW FORMAT SERDE
    'org.apache.hadoop.hive.ql.io.orc.OrcSerde'
    WITH SERDEPROPERTIES
    ('field.delim'='\\t', 'line.delim'='\\n', 'serialization.format'='\\t')
    STORED AS INPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat'
    OUTPUTFORMAT
    'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
    LOCATION
    's3n://{bucket}/data/{path}/{database}/{table_name}'
    TBLPROPERTIES ('EXTERNAL'='FALSE','bucketing_version'='2','orc.compress'='SNAPPY')'''

    # 替换insert overwrite
    insert_replace = s3_location_info + ''';
    insert'''

    result = ''''''

    def __init__(self, *args, **kwargs):
        config = Config()
        self.bucket = config.get_config('bucket')
        self.path = config.get_config('path')
        self.database = config.get_config('database')
        self.host = config.get_config('host')
        self.backup_host = config.get_config('backup_host')
        self.username = config.get_config('username')
        self.port = config.get_config('port')
        self.alarm_url = config.get_config('alarm_url')

    def build(self, hql):
        """
        传入HQL，进行构建，偶尔有设置参数等SQL放入
        :param hql:HQL
        :return:返回当前类对象
        """
        self.result = self.result + hql
        return self

    def create(self, table_name, hql):
        """
        传入HQL，进行构建，主要用于创建表，无需关注s3存储
        :param table_name:表名
        :param hql:HQL
        :return:返回当前类对象
        """
        hql = hql.replace('insert', self.insert_replace, 1) + ''';'''
        self.result = self.result + hql.format(bucket=self.bucket,
                                               path=self.path,
                                               database=self.database,
                                               table_name=table_name)
        return self

    def create_as(self, table_name, query_hql):
        """
        构建中间表
        :param table_name:表名
        :param query_hql:查询HQL
        :return:返回建表SQL语句
        """
        self.result = self.result + self.create_as_table.format(bucket=self.bucket,
                                                                path=self.path,
                                                                database=self.database,
                                                                table_name=table_name,
                                                                query_hql=query_hql)
        return self

    def create_pt(self, table_name, column_info, partition_info, insert_sql):
        """
        构建分区表
        :param table_name:表名
        :param column_info:列信息
        :param insert_sql:insert HQL
        :param partition_info:分区信息
        :return:返回建表SQL语句
        """
        self.result = self.result + self.create_partition_table.format(bucket=self.bucket,
                                                                       path=self.path,
                                                                       database=self.database,
                                                                       table_name=table_name,
                                                                       insert_sql=insert_sql,
                                                                       partition_info=partition_info,
                                                                       column_info=column_info)
        return self

    def create_default_pt(self, table_name, column_info, insert_sql):
        """
        构建分区表
        :param table_name:表名
        :param column_info:列信息
        :param insert_sql:insert HQL
        :return:返回建表SQL语句
        """
        self.result = self.result + self.create_default_partition_table.format(bucket=self.bucket,
                                                                               path=self.path,
                                                                               database=self.database,
                                                                               table_name=table_name,
                                                                               insert_sql=insert_sql,
                                                                               column_info=column_info)
        return self

    def insert_default_pt(self, table_name, column_info, yyyymmdd, query_sql):
        """
        构建分区表并带insert
        :param table_name:表名
        :param column_info:列信息
        :param query_sql:查询HQL
        :param yyyymmdd:分区
        :return:返回建表SQL语句
        """
        self.result = self.result + self.create_default_partition_table_and_insert.format(bucket=self.bucket,
                                                                                          path=self.path,
                                                                                          database=self.database,
                                                                                          table_name=table_name,
                                                                                          query_sql=query_sql,
                                                                                          yyyymmdd=yyyymmdd,
                                                                                          column_info=column_info)
        return self

    def get_result(self):
        """
        :return:返回结果
        """
        return self.result

    def exec(self, message, users=None):
        """
        执行HQL
        :param message:告警信息
        :return:返回执行结果
        """
        print(self.result)
        exec_result = run_hive(self.result, self.host, self.backup_host, self.port, self.username, message,
                               self.alarm_url, users)
        self.result = ''''''
        return exec_result

    def exec_hive(self, hql, message, users=None):
        """
        执行HQL
        :param message:告警信息
        :return:返回执行结果
        """
        print(hql)
        return run_hive(hql, self.host, self.backup_host, self.port, self.username, message, self.alarm_url, users)

    def get_partition(self, table, index, message):
        """
        获取partition
        :param table: 表
        :param index: 下标
        :param message: 信息
        :return: 返回分区值
        """
        sql = '''show partitions ''' + table

        latest_partition = self.exec_hive(sql, message)
        if latest_partition:
            return sorted(latest_partition, reverse=True)[int(index)][0].split('=')[1]
        return ''

    def get_last_partition(self, table, message):
        """
        获取最后一个partition
        :param table: 表
        :param message: 信息
        :return: 返回分区值
        """
        return self.get_partition(table, 0, message)


"""
时间工具类
author zhouyuqin
date 2021-12-16
"""
NEW_YORK = tz.gettz('America/New_York')
UTC = tz.gettz('UTC')
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
WINTER_TIME = ' 05:00:00'
SUMMER_TIME = ' 04:00:00'
# 冬季标志
WINTER_FLAG = False
# 夏季标志
SUMMER_FLAG = True


def get_eastern_curr_time():
    """
    获取美东目前时间
    :return:返回美东时间
    """
    return datetime.datetime.now(NEW_YORK).strftime(DATETIME_FORMAT)


def get_eastern_curr_date():
    """
    获取美东目前日期
    :return:返回美东日期
    """
    return datetime.datetime.now(NEW_YORK).strftime(DATE_FORMAT)


def get_eastern_time_offset(offset):
    """
    返回距离当前美东时间的前几日
    :param offset:偏移量
    :return:返回美东时间
    """
    return (datetime.datetime.now(NEW_YORK)
            - datetime.timedelta(int(offset))).strftime(DATETIME_FORMAT)


def get_utc_curr_time():
    """
    获取UTC目前时间
    :return:返回UTC时间
    """
    return datetime.datetime.now(UTC).strftime(DATETIME_FORMAT)


def get_utc_curr_date():
    """
    获取UTC目前日期
    :return:返回UTC目前日期
    """
    return datetime.datetime.now(UTC).strftime(DATE_FORMAT)


def get_utc_time_offset(offset):
    """
    返回距离当前UCT时间的前几日
    :param offset:偏移量
    :return:返回UTC时间
    """
    return (datetime.datetime.now(UTC)
            - datetime.timedelta(int(offset))).strftime(DATETIME_FORMAT)


def get_eastern_year():
    """
    获取美东时间年
    :return:返回美东时间的年
    """
    return datetime.datetime.now(NEW_YORK).year


def get_eastern_month():
    """
    获取美东时间月份
    :return:返回美东时间的月份
    """
    return datetime.datetime.now(NEW_YORK).month


def check_eastern_timezone(eastern_date):
    """
    美东时间时区检查,只支持yyyy-mm-dd格式日期
    :param eastern_date: 美东日期
    :return:WINTER_FLAG:夏令时，False：夏令时
    """
    if len(eastern_date) != 10:
        raise Exception('Illegal date format')
    dates = eastern_date.split("-")

    dt = datetime.datetime(int(dates[0]), int(dates[1]), int(dates[2]), 0, 0, 0, 0, NEW_YORK)
    dt_to_utc = dt.replace(tzinfo=datetime.timezone.utc)
    if int((dt - dt_to_utc).total_seconds()) == 18000:
        return WINTER_FLAG
    return SUMMER_FLAG


def get_eastern_date_to_utc_time(eastern_date):
    """
    美东日期转UTC时间，只支持日期转标准时间
    :param eastern_date: 美东日期
    :return:返回UTC时间
    """
    if check_eastern_timezone(eastern_date):
        return eastern_date + SUMMER_TIME
    return eastern_date + WINTER_TIME
