# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from datetime import datetime
import sys
import util
import lookuptables


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
topics_without_ids = []

try:

    #######
    # dnb_item
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_item`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_item')

    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_item` (`id` varchar(12) NOT NULL," \
              " `title` text, `title_add` text, `year` smallint unsigned, content text," \
              " `toc` text, publisher text, primary key (id), index (year) )" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_item')

    print('open file and read line by line')
    l = 0
    with open('export/errorlog.txt', 'w+') as newFile:
        with open('data/bib-records.json') as f:
            # with open('export/bib-records-reduced.json') as f:
            for line in f:
                entry = json.loads(line)

                j = 0
                for i in util.seq_iter(entry):
                    j += 1

                if j > 2:
                    id_ = entry['003@'][0]['0'].lower()

                    pub_year = ''

                    try:
                        entry['011E']
                    except KeyError:
                        try:
                            pub_year = entry['011@'][0]['a']
                        except KeyError:
                            pass
                    else:
                        try:
                            pub_year = entry['011E'][0]['r']
                        except KeyError:
                            pass

                    year = util.getYear(pub_year)

                    title = ''
                    tadd = ''
                    try:
                        entry['021A'][0]
                    except KeyError:
                        pass
                    else:
                        try:
                            title = entry['021A'][0]['a']
                        except KeyError:
                            pass
                        try:
                            tadd = entry['021A'][0]['d']
                        except KeyError:
                            pass

                    content = ''
                    try:
                        entry['013D'][0]
                    except KeyError:
                        pass
                    else:
                        try:
                            content = entry['013D'][0]['a']
                        except KeyError:
                            pass

                    toc = ''
                    try:
                        entry['047I'][0]
                    except KeyError:
                        pass
                    else:
                        try:
                            toc = entry['047I'][0]['u']
                        except KeyError:
                            pass

                    publisher = ''
                    try:
                        entry['033A']
                    except KeyError:
                        pass
                    else:
                        va = []
                        for i in entry['033A']:
                            va.append({'name': i.setdefault('n', ''),
                                       'ort': i.setdefault('p', '')})
                        publisher = str(va)

                    # ------------------------------------
                    with connection.cursor() as cursor:
                        # Create a new record
                        sql = "INSERT INTO `dnb_item` (`id`, `title`, `title_add`, `year`, `content`, `toc`, publisher) " \
                              "VALUES (%s, %s, %s, %s, %s, %s)"

                        try:
                            cursor.execute(
                                sql, (id_, title, tadd, year, toc, content, publisher))
                        # except pymysql.err.InternalError:
                        except:
                            newFile.write('insert into dnb_item with values')
                            err = (id_, title, tadd, year, toc, publisher)
                            newFile.write(
                                str(err))
                            newFile.write(str(sys.exc_info()[0]))
                            # print('\n \n error in insert dnb_item')
                            # print(entry)

                connection.commit()
                uptime = str(datetime.now() - startTime).split('.')[0]
                l += 1
                # sys.stdout.write('\033[2J\033[1;1H') # cleans complete
                # screen
                sys.stdout.write('\033[K\033[1;1H')  # cleans line
                sys.stdout.write(
                    'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
                sys.stdout.flush()
    newFile.close
    print('\n finished loading dataset')

finally:
    connection.close()
