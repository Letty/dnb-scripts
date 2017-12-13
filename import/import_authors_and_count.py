# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from datetime import datetime
import sys

sys.path.insert(1, '..')
from lib import util


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


startTime = datetime.now()

connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='',
                             db='dnb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('Connection to database established')

try:

    # drop table
    with connection.cursor() as cursor:
        sql = "DROP TABLE IF EXISTS `dnb_author_count`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_author_count')

    # create table
    with connection.cursor() as cursor:

        sql = "CREATE TABLE IF NOT EXISTS `dnb_author_count` (`id`  varchar(13) NOT NULL," \
              " `name` MEDIUMTEXT, `lastname` MEDIUMTEXT, date_of_birth varchar(50), date_of_death varchar(50), " \
              + "count MEDIUMINT UNSIGNED, PRIMARY KEY(id)) ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_author_count')

    print('open file and read line by line')

    with open('../export/authors_full_lifetime.json') as f:
        data = json.load(f)

        author = []
        for key in util.seq_iter(data):
            b = ''
            d = ''
            if 'birth' in data:
                b = data[key]['birth']
            if 'death' in data:
                d = data[key]['death']

            author.append([key, data[key]['name'],
                           data[key]['lastname'], b,
                           d, data[key]['count']])
        i = 0
        for k in author:
            id_ = k[0]
            name = k[1]
            lastname = k[2]
            birth = k[3]
            death = k[4]
            count = k[5]
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `dnb_author_count` (`id`, `name`, `lastname`, `date_of_birth`, `date_of_death`, `count`) " \
                      "VALUES (%s, %s, %s,%s, %s,%s)"
                try:
                    cursor.execute(
                        sql, (id_, name, lastname, birth, death, count))
                except:
                    print('\n \n')
                    print(k)

            connection.commit()
            uptime = str(datetime.now() - startTime).split('.')[0]
            i += 1
            sys.stdout.write('\033[K\033[1;1H')  # cleans line
            sys.stdout.write(
                'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, i))
            sys.stdout.flush()

    print('\n finished loading dataset')

finally:
    connection.close()
