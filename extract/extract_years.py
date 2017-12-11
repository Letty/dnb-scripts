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

print('open file and read line by line')
l = 0
# Year - Author (name) - Author (id) - topics
years = {}
year_array = []


with open('../export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)

        try:
            entry['011E']
        except KeyError:
            try:
                entry['011@']
            except KeyError:
                pass
            else:
                for y in entry['011@']:
                    try:
                        y['a']
                    except KeyError:
                        pass
                    else:
                        try:
                            years[y['a']]
                        except KeyError:
                            years[y['a']] = 1
                        else:
                            years[y['a']] += 1
        else:
            for y in entry['011E']:
                try:
                    y['r']
                except KeyError:
                    pass
                else:
                    try:
                        years[y['r']]
                    except KeyError:
                        years[y['r']] = 1
                    else:
                        years[y['r']] += 1

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('../export/years.json', mode='w') as fi:
    fi.write(json.dumps(years, indent='\t', sort_keys='true'))
