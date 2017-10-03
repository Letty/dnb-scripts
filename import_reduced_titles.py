# -*- coding: utf-8 -*-
import pymysql.cursors
import json
import re
from datetime import datetime
import sys
import util
import lookuptables


def seq_iter(obj):
    return obj if isinstance(obj, dict) else range(len(obj))


def getYear(st):
    p = re.findall('(\d{4})', st)
    if (len(p) == 0):
        return 0
    else:
        return int(p[0])


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
              " `title` text, `title_add` text, `year` smallint unsigned, " \
              " `toc` text, publisher text, primary key (id), index (year) )" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_item')

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
    with open('data/bib-records.json') as f:
        # with open('export/bib-records-reduced.json') as f:
        for line in f:
            entry = json.loads(line)

            #  16.564.763 ['003@'] Datensatz ID
            #      73.470 ['011E'] Entstehungsdatum, sonstige Datumsangaben
            #  15.623.024 ['011@'] Erscheinungsjahr
            #  13.477.159 ['021A'] Hauptsachtitel, Zusätze, Parallelsachtitel, Verfasserangabe
            #   8.675.529 ['028A'] 1.Verfasser
            #     768.701 ['044F'] Schlagwörter aus Altdaten der Deutschen Nationalbibliothek
            #     475.254 ['044G'] Literarische Gattung
            #     143.756 ['044H'] Automatisch vergegebenes Schlagwort
            #     259.970 ['044K'] GND-Schlagwörter
            #   4.350.351 ['044N'] Deskriptoren aus einem Thesaurus
            #   1.066.192 ['045C'] 2. + 3.maschinell vergebene Sachgruppen
            #   4.647.455 ['045E'] Sachgruppen der Deutschen Nationalbibliografie
            #     110.813 ['045G'] DDC-Notation: Vollständige Notation
            #   2.621.471 ['041A']      1.Schlagwortfolge 1.Element
            #   2.355.042 ['041A/01']   1.Schlagwortfolge 2.Element
            #   1.556.937 ['041A/02']   1.Schlagwortfolge 3.Element
            #     870.757 ['041A/03']   1.Schlagwortfolge 4.Element
            #   1.752.704 ['041A/08']  Vorgegebene(s) Permutationsmuster zur 1. Schlagwortfolge
            #   2.625.849 ['041A/09']  Angaben zur 1. Schlagwortfolge

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

            year = getYear(pub_year)

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

            keywords = []

            util.checkField(entry, '044N', ['a'], keywords, False)
            util.checkField(entry, '044H', ['a'], keywords, False)
            util.checkField(entry, '044K', ['a'], keywords, False)
            util.checkField(entry, '045G', ['a'], keywords, False)
            util.checkField(entry, '044F', ['a', 'f'], keywords, False)
            util.checkField(entry, '045C', ['f', 'g'], keywords, False)
            util.checkField(
                entry, '045E', ['e'], keywords, lookuptables.lookupSachgruppe)

            util.findKeywords(keywords, entry, '041A')
            util.findKeywords(keywords, entry, '041A/01')
            util.findKeywords(keywords, entry, '041A/02')
            util.findKeywords(keywords, entry, '041A/03')
            util.findKeywords(keywords, entry, '041A/08')
            util.findKeywords(keywords, entry, '041A/09')

            # ------------------------------------
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `dnb_item` (`id`, `title`, `title_add`, `year`, `toc`, publisher) " \
                      "VALUES (%s, %s, %s, %s, %s, %s)"

                try:
                    cursor.execute(sql,
                                   (id_, title, tadd, year, toc, publisher))
                # except pymysql.err.InternalError:
                except:
                    print('\n \n')
                    print(entry)

            connection.commit()
            uptime = str(datetime.now() - startTime).split('.')[0]
            l += 1
            # sys.stdout.write('\033[2J\033[1;1H') # cleans complete screen
            sys.stdout.write('\033[K\033[1;1H')  # cleans line
            sys.stdout.write(
                'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
            sys.stdout.flush()

    print('\n finished loading dataset')

finally:
    connection.close()
