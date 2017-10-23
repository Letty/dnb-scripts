# -*- coding: utf-8 -*-
import pymysql.cursors
import json
import re
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
topics_lookuptable = {}

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
    # dnb_item_topic
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_item_topic`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_item_topic')
    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_item_topic` (`i_id` varchar(12) NOT NULL," \
              " `t_id` MEDIUMINT UNSIGNED NOT NULL, `year` smallint unsigned, " \
              " primary key (i_id, t_id), index (year) )" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_item_topic')

    #######
    # dnb_author_topic
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_author_topic`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_author_topic')
    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_author_topic` (`a_id` varchar(12) NOT NULL," \
              " `t_id` MEDIUMINT UNSIGNED NOT NULL, `count` mediumint unsigned, " \
              " primary key (a_id, t_id))" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_author_topic')

    #######
    # dnb_topic_topic
    #######
    # drop table
    with connection.cursor() as cursor:

        sql = "DROP TABLE IF EXISTS `dnb_topic_topic`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_topic_topic')
    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_topic_topic` (`t_id1` MEDIUMINT UNSIGNED NOT NULL," \
              " `t_id2` MEDIUMINT UNSIGNED NOT NULL, `count` mediumint unsigned, " \
              " primary key (t_id1, t_id2))" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_topic_topic')

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
    with open('export/errorlog_relation.txt', 'w+') as newFile:
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

                    author_ids = []
                    util.getAuthorId(entry, '028A', author_ids)
                    util.getAuthorId(entry, '028C', author_ids)

                    keywords = []

                    util.checkField(entry, '044N', ['a'], keywords, False)
                    util.checkField(entry, '044H', ['a'], keywords, False)
                    util.checkField(entry, '044K', ['a'], keywords, False)
                    util.checkField(entry, '045G', ['a'], keywords, False)

                    util.checkFieldDDC(entry, '045G', ['a'],
                                       current_topics, lookuptables.lookupDDC)
                    util.checkField(entry, '045C', ['f', 'g'],
                                    current_topics, lookuptables.lookupSachgruppe)
                    util.checkFieldDDC(entry, '045E', ['e'],
                                       current_topics, lookuptables.lookupDDC)

                    util.findKeywords(keywords, entry, '041A')
                    util.findKeywords(keywords, entry, '041A/01')
                    util.findKeywords(keywords, entry, '041A/02')
                    util.findKeywords(keywords, entry, '041A/03')
                    util.findKeywords(keywords, entry, '041A/08')
                    util.findKeywords(keywords, entry, '041A/09')

                    # ------------------------------------

                    topic_ids = []
                    for k in keywords:
                        try:
                            topics_lookuptable[k]
                        except KeyError:
                            with connection.cursor() as cursor:
                                # Create a new record
                                sql = "select `id` from `dnb_topic_count` where `keyword`=%s"
                                cursor.execute(sql, (k))
                                r = cursor.fetchone()
                                if r == None:
                                    topics_without_ids.append(k)
                                else:
                                    topics_lookuptable[k] = r['id']
                                    topic_ids.append(r['id'])
                        else:
                            topic_ids.append(topics_lookuptable[k])

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

                    for t in topic_ids:
                        with connection.cursor() as cursor:
                            # Create a new record
                            sql = "INSERT INTO `dnb_item_topic` (`i_id`, `t_id`, `year`) " \
                                  "VALUES (%s, %s, %s)"

                            try:
                                cursor.execute(sql, (id_, t, year))
                            # except pymysql.err.InternalError:
                            except:
                                newFile.write(
                                    'insert into dnb_item_topic with values')
                                err = (id_, t, year)
                                newFile.write(str(err))
                                newFile.write(str(sys.exc_info()[0]))
                                # print('\n \n error in insert dnb_item_item')
                                # print(str(sys.exc_info()[0]))

                    for a in author_ids:
                        for t in topic_ids:
                            with connection.cursor() as cursor:
                                # Create a new record
                                sql = "INSERT INTO `dnb_author_topic` (`a_id`, `t_id`, `count`) " \
                                      "VALUES (%s, %s, %s) on duplicate key update `count`=`count`+1"

                                try:
                                    cursor.execute(sql, (a, t, 1))
                                # except pymysql.err.InternalError:
                                except:
                                    newFile.write(
                                        'insert into dnb_author_topic with values')
                                    err = (a, t)
                                    newFile.write(str(err))
                                    newFile.write(str(sys.exc_info()[0]))
                                    # print('\n \n error in insert dnb_author_topic')
                                    # print(entry)

                                    # nicht klar obs funzt
                    if len(topic_ids) > 1:
                        i = 1
                        for t in topic_ids:
                            if i != len(topic_ids) - 1:
                                with connection.cursor() as cursor:
                                    # Create a new record
                                    sql = "INSERT INTO `dnb_topic_topic` (`t_id1`, `t_id2`, `count`) " \
                                          "VALUES (%s, %s, %s) on duplicate key update `count`=`count`+1"

                                    try:
                                        cursor.execute(
                                            sql, (t, topic_ids[i], 1))
                                    # except pymysql.err.InternalError:
                                    except:
                                        newFile.write(
                                            'insert into dnb_topic_topic with values')
                                        err = (t, topic_ids[i])
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
