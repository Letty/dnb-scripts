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
authors = []
with open('export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)

        id_ = entry['003@'][0]['0'].lower()

        try:
            entry['028A']
        except KeyError:
            pass
        else:
            for e in entry['028A']:
                try:
                    e['9']
                except KeyError:
                    pass
                else:
                    authors.append([id_, e['9'].lower()])

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('export/title_author_relation.json', mode='w') as fi:
    fi.write(json.dumps(authors, indent='\t', sort_keys='true'))
