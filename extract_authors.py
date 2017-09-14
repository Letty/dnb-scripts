# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sys
import util


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

print('open file and read line by line')
l = 0
# Year - Author (name) - Author (id) - topics
authors = {}


with open('export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)
        try:
            entry['028A']
        except KeyError:
            pass
        else:
            try:
                entry['028A'][0]['9']
            except KeyError:
                pass
            else:
                try:
                    authors[entry['028A'][0]['9'].lower()]
                except KeyError:
                    authors[entry['028A'][0]['9'].lower()] = {'count': 1,
                                                              'name': util.extractAuthorName(entry['028A'][0])}
                else:
                    authors[entry['028A'][0]['9'].lower()]['count'] += 1

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('export/authors.json', mode='w') as fi:
    fi.write(json.dumps(authors, indent='\t', sort_keys='true'))
