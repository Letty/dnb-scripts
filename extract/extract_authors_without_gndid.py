# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sys


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
# Autoren ohne GND ID:  8.459.267
# Autoren ohne GND ID:  7.659.213
#                      16.118.480
# Autoren mit einer ID: 8.905.518 (aus dem Script, aber scheinbar nicht
# korrekt)

print('open file and read line by line')
l = 0
author = 0
with open('../data/bib-records.json') as f:
    for line in f:
        entry = json.loads(line)
        #   8.675.529 ['028A'] 1.Verfasser

        try:
            entry['028A']
        except KeyError:
            author += 1
            pass
        else:
            try:
                entry['028A'][0]['9']
            except KeyError:
                author += 1
                pass

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()

print('\n \n finished loading dataset')
print('Autoren ohne GND ID: %i' % (author))
# with open('../export/content.json', mode='w') as fi:
#     fi.write(../json.dumps(content, indent='\t', sort_keys='true'))
