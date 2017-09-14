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
                             db='dnb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('\n Connection to database established')

try:

    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_reduced_topic_count`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_reduced_topic_count')

    # create table
    with connection.cursor() as cursor:

        # * datensatz id l['003@'][0]['0'] -
        # * gnd nummer für links ['007K'][0]['0']
        # array: ddc notation ['037G'][index]['c'] // wie stellt man das gut dar?
        # * Begriff ['041A']
        # + ['041A'][0][a] Sachbegriff
        # + ['041A'][0][g] Sachbegriff Zusatz
        # + ['041A'][0][x] Sachbegriff Allgemeine  Unterteilung
        #  gnd klassifikation ['042A']['a'][index]
        # * typ ['004B'][0]['a'] .. lookup.lookUp004B[code]

        # folgende verwandte begriffe wenn $4=vbal ist:
        # array: verwandte begriffe  ['065R'] - geografikum -> das müsste theoretisch eine tabelle sein
        # a - geografikum
        # g - zusatz
        # z - geografischer untertitel
        # x - allg. untertitel
        # 4 - komischer code für beziehung.. kackteil.. muss auch außeinandergeprökelt werden
        # array: verwandte begriffe ['022R']  Einheitstitel - Beziehung
        # a t g m n p s x f r k h o
        # array: verwandte begriffe (a n g b x) ['029R'] Körperschaft - Beziehung
        # array: verwandte begriffe (P a d n d c l) ['028R'] Person - Beziehung
        # verwandte begriffe (a n d c g b x) ['030R'] Konferenz - Beziehung

        sql = "CREATE TABLE IF NOT EXISTS `dnb_reduced_topic_count` (`id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT," \
              " `keyword` TEXT, count MEDIUMINT UNSIGNED, PRIMARY KEY(id)) " \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)
    connection.commit()
    print('create table dnb_reduced_topic_count')

    print('open file and read line by line')
    i = 0
    with open('export/topics.json') as f:
        data = json.load(f)

        kw = []
        for key in util.seq_iter(data):
            kw.append([key, data[key]])

        for k in kw:
            keyword = k[0]
            count = k[1]
            with connection.cursor() as cursor:
                # Create a new record
                i += 1
                sql = "INSERT INTO `dnb_reduced_topic_count` (`keyword`, `count` ) " \
                      "VALUES (%s, %s)"
                try:
                    cursor.execute(sql, (keyword, count))
                except pymysql.err.InternalError:
                    print('\n \n')
                    print(entry)

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
