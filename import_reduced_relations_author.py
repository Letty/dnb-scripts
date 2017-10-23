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
                             db='dnb2',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('\n Connection to database established')

try:

    #######
    # dnb_author_item
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_author_item`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_author_item')
    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_author_item` (`a_id` varchar(12) NOT NULL," \
              " `i_id` varchar(12) NOT NULL, `year` smallint unsigned, " \
              " primary key (a_id, i_id), index (year) )" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_author_item')

    #######
    # dnb_author_author
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_author_author`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_author_author')
    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_author_author` (`a_id1` varchar(12) NOT NULL," \
              " `a_id2` varchar(12) NOT NULL, `count` mediumint unsigned, " \
              " primary key (a_id1, a_id2))" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_topic_topic')

    print('open file and read line by line')
    l = 0
    with open('export/errorlog_relation_authors_reduced.txt', 'w+') as newFile:
        with open('export/bib-records-reduced.json') as f:
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

                    author_ids = []
                    util.getAuthorId(entry, '028A', author_ids)
                    util.getAuthorId(entry, '028C', author_ids)

                    keywords = []

                    util.checkField(entry, '044N', ['a'], keywords, False)
                    util.checkField(entry, '044H', ['a'], keywords, False)
                    util.checkField(entry, '044K', ['a'], keywords, False)
                    util.checkField(entry, '045G', ['a'], keywords, False)

                    util.checkFieldDDC(entry, '045G', ['a'],
                                       keywords, lookuptables.lookupDDC)
                    util.checkField(entry, '045C', ['f', 'g'],
                                    keywords, lookuptables.lookupSachgruppe)
                    util.checkFieldDDC(entry, '045E', ['e'],
                                       keywords, lookuptables.lookupDDC)

                    util.findKeywords(keywords, entry, '041A')
                    util.findKeywords(keywords, entry, '041A/01')
                    util.findKeywords(keywords, entry, '041A/02')
                    util.findKeywords(keywords, entry, '041A/03')
                    util.findKeywords(keywords, entry, '041A/08')
                    util.findKeywords(keywords, entry, '041A/09')

                    # ------------------------------------

                    for a_id in author_ids:
                        with connection.cursor() as cursor:
                            # Create a new record
                            sql = "INSERT INTO `dnb_author_item` (`a_id`, `i_id`, `year`) " \
                                  "VALUES (%s, %s, %s)"

                            try:
                                cursor.execute(sql, (a_id, id_, year))
                            # except pymysql.err.InternalError:
                            except:
                                newFile.write(
                                    'insert into dnb_author_item with values')
                                err = (a_id, id_, year)
                                newFile.write(str(err))
                                newFile.write(str(sys.exc_info()[0]))
                                # print('\n \n error in insert dnb_author_item')
                                # print(entry)

                    # nicht klar obs funzt
                    if len(author_ids) > 1:
                        i = 1
                        for a in author_ids:
                            if i != len(author_ids) - 1:
                                with connection.cursor() as cursor:
                                    # Create a new record
                                    sql = "INSERT INTO `dnb_author_author` (`a_id1`, `a_id2`, `count`) " \
                                          "VALUES (%s, %s, %s) on duplicate key update `count`=`count`+1"
                                    # ON DUPLICATE KEY UPDATE

                                    try:
                                        cursor.execute(
                                            sql, (a, author_ids[i], 1))
                                    # except pymysql.err.InternalError:
                                    except:
                                        newFile.write(
                                            'insert into dnb_author_author with values')
                                        err = (a, author_ids[i])
                                        newFile.write(str(err))
                                        newFile.write(
                                            str(sys.exc_info()[0]))
                                        # print('\n \n error in insert dnb_author_item')
                                        # print(entry)
                                i += 1

                connection.commit()
                uptime = str(datetime.now() - startTime).split('.')[0]
                l += 1
                # sys.stdout.write('\033[2J\033[1;1H') # cleans complete screen
                sys.stdout.write('\033[K\033[1;1H')  # cleans line
                sys.stdout.write(
                    'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
                sys.stdout.flush()
    newFile.close
    print('\n finished loading dataset')

finally:
    connection.close()
