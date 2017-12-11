# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sys
import util


def seq_iter(obj):
    return obj if isinstance(obj, dict) else range(len(obj))


def extract_author_from_field(entry, fieldId, aut_dict):
    try:
        entry[fieldId]
    except KeyError:
        pass
    else:
        try:
            entry[fieldId][0]['9']
        except KeyError:
            pass
        else:
            try:
                aut_dict[entry[fieldId][0]['9'].lower()]
            except KeyError:
                aut = {'count': 1, 'name': '', 'lastname': ''}

                try:
                    aut['name'] = entry[fieldId][0]['d']
                except KeyError:
                    pass

                try:
                    aut['lastname'] = entry[fieldId][0]['a']
                except KeyError:
                    pass

                aut_dict[entry[fieldId][0]['9'].lower()] = aut

            else:
                if aut_dict[entry[fieldId][0]['9'].lower()]['name'] == '':
                    try:
                        aut_dict[entry[fieldId][0]['9'].lower()]['name'] = entry[
                            fieldId][0]['d']
                    except KeyError:
                        pass

                if aut_dict[entry[fieldId][0]['9'].lower()]['lastname'] == '':
                    try:
                        aut_dict[entry[fieldId][0]['9'].lower()]['lastname'] = entry[
                            fieldId][0]['a']
                    except KeyError:
                        pass

                aut_dict[entry[fieldId][0]['9'].lower()]['count'] += 1


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

print('open file and read line by line')
l = 0
# Year - Author (name) - Author (id) - topics
authors = {}

# todo -> lebensdaten - Geburt + Tod aus der gnd nach dem hinzufügen aus
# den titeldaten
# with open('../data/bib-records.json') as f:
with open('../export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)

        # 028C, selbes schema wie 028A

        extract_author_from_field(entry, '028A', authors)
        extract_author_from_field(entry, '028C', authors)

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('../export/authors.json', mode='w') as fi:
    fi.write(json.dumps(authors, indent='\t', sort_keys='true'))
