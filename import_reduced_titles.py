# -*- coding: utf-8 -*-
import pymysql.cursors
import json
from datetime import datetime
import sys
import util
import lookuptables


def seq_iter(obj):
    return obj if isinstance(obj, dict) else range(len(obj))


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

        sql = "DROP TABLE IF EXISTS `dnb_reduced_title`"
        cursor.execute(sql)
    connection.commit()
    print('drop table dnb_reduced_title')

    # create table
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS `dnb_reduced_title` (`key_id` varchar(12) NOT NULL," \
              " `title` longtext, `title_add` longtext, `year` char(35), `year_end` char(35)," \
              " `author_firstname` varchar(200), `author_lastname` varchar(200)," \
              " `author_gndid` varchar(20), `keywords` longtext)" \
              + "ENGINE=InnoDB DEFAULT CHARSET=utf8"
        cursor.execute(sql)

    connection.commit()
    print('create table dnb_title')

    print('open file and read line by line')
    l = 0
    with open('export/bib-records-reduced.json') as f:
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

            id = entry['003@'][0]['0'].lower()

            vo = ''
            vj = ''

            try:
                entry['011E']
            except KeyError:
                try:
                    vo = entry['011@'][0]['a']
                except KeyError:
                    pass
                try:
                    vj = entry['011@'][0]['b']
                except KeyError:
                    pass
            else:
                try:
                    vo = entry['011E'][0]['r']
                except KeyError:
                    pass

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

            # logisch, der erste Autor kann auch aus 3 Autoren bestehen..
            # dh hier muss ich über ein Array gehen
            name = ''
            vorname = ''
            author_id = ''
            author_all = ''  # noch nicht in db
            try:
                entry['028A']
            except KeyError:
                pass
            else:
                author_all = entry['028A']
                name = entry['028A'][0].setdefault('a', '')
                vorname = entry['028A'][0].setdefault('d', '')
                author_id = entry['028A'][0].setdefault('9', '').lower()

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
                sql = "INSERT INTO `dnb_reduced_title` (`key_id`, `title`, `title_add`, `year`, `year_end`, " \
                      " `author_firstname`, `author_lastname`, `author_gndid`, `keywords`) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                try:
                    cursor.execute(sql,
                                   (id, title, tadd, vo, vj, vorname, name, author_id, str(keywords)))
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
