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

print('open file and read line by line')
l = 0
authors = {}

with open('../data/bib-records.json') as f:
    # with open('../export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)

        # 028C, selbes schema wie 028A

        util.extract_author_from_field(entry, '028A', authors)
        util.extract_author_from_field(entry, '028C', authors)

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('../export/authors_full.json', mode='w') as fi:
    fi.write(json.dumps(authors, indent='\t', sort_keys='true'))
