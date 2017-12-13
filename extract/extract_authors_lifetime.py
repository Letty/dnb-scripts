# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sys
sys.path.insert(1, '..')
from lib import util


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

with open('../export/authors_full.json', 'r') as af:
    content = af.read()
    # print(content)

authors = json.loads(content)
auth = {}

print('open file and read line by line')
l = 0
with open('../data/tp-records.json') as f:
    for line in f:
        entry = json.loads(line)

        id_ = entry['007K'][0]['0'].lower()

        util.extract_author_from_field(entry, '028A', authors)

        try:
            entry['060R']
        except KeyError:
            pass
        else:
            try:
                authors[id_]
            except KeyError:
                pass
            else:
                for dates in entry['060R']:
                    try:
                        dates['4']
                    except KeyError:
                        pass
                    else:
                        if dates['4'] == 'datx':
                            try:
                                dates['a']
                            except KeyError:
                                pass
                            else:
                                authors[id_]['birth'] = dates['a']
                            try:
                                dates['b']
                            except KeyError:
                                pass
                            else:
                                authors[id_]['death'] = dates['b']

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('../export/authors_full2.json', mode='w') as fi:
    fi.write(json.dumps(authors, indent='\t', sort_keys='False'))
