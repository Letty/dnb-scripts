# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from datetime import datetime
import sys
import util


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
                             db='dnb2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('Connection to database established')

try:

        # sql = "CREATE TABLE IF NOT EXISTS `dnb_author_count` (`id`  varchar(13) NOT NULL," \
        #       " `name` MEDIUMTEXT, `lastname` MEDIUMTEXT, date_of_birth varchar(50), date_of_death varchar(50), " \
        #       + "count MEDIUMINT UNSIGNED, PRIMARY KEY(id)) ENGINE=InnoDB DEFAULT CHARSET=utf8"

    print('open file and read line by line')

    with open('export/authors_lifetime.json') as f:
        data = json.load(f)

        author = []
        for key in util.seq_iter(data):
            b = ''
            d = ''

            try:
                data[key]['birth']
            except KeyError:
                pass
            else:
                b = data[key]['birth']

            try:
                data[key]['death']
            except KeyError:
                pass
            else:
                d = data[key]['death']

            author.append([key, b, d])
        i = 0
        for k in author:
            id_ = k[0]
            birth = k[1]
            death = k[2]
            # print(data[key])

            with connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE dnb_author_count SET date_of_birth=%s, date_of_death=%s WHERE id=%s"
                try:
                    cursor.execute(sql, (birth, death, id_))
                except:
                    print('\n \n')
                    print(k)

            connection.commit()
            uptime = str(datetime.now() - startTime).split('.')[0]
            i += 1
            # sys.stdout.write('\033[2J\033[1;1H') # cleans complete screen
            sys.stdout.write('\033[K\033[1;1H')  # cleans line
            sys.stdout.write(
                'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, i))
            sys.stdout.flush()

    print('\n finished loading dataset')

finally:
    connection.close()
