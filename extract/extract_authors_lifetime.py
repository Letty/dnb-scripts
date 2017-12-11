# -*- coding: utf-8 -*-
import json
from datetime import datetime
import sys
import util


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

with open('../export/authors.json', 'r') as af:
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
        a = {id: id_}

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
                            auth[id_] = {}
                            try:
                                dates['a']
                            except KeyError:
                                pass
                            else:
                                auth[id_]['birth'] = dates['a']
                            try:
                                dates['b']
                            except KeyError:
                                pass
                            else:
                                auth[id_]['death'] = dates['b']
        # lifetime
# time = r.findall(".//*[@id='060R']", ns)
# for t in time:
#     lifetime = {}
#     isLifetime = False
#     for it in t.iter():
#         # birth
#         if it.get('id') == 'a':
#             lifetime['birth'] = it.text
#         if it.get('id') == 'b':
#             lifetime['death'] = it.text
#         if it.get('id') == 'v':
#             lifetime['additional-notes'] = it.text
#         if it.get('id') == '4' and it.text == 'datx':
#             isLifetime = True

#     if isLifetime:
#         person['lifetime'] = lifetime

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()


print('\n \n finished loading dataset')

with open('../export/authors_lifetime.json', mode='w') as fi:
    fi.write(json.dumps(auth, indent='\t', sort_keys='False'))
