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
content = {
    "Bewegungsnotation": 0,
    "Computerdaten": 0,
    "Computerprogramm": 0,
    "Gera\u0308usche": 0,
    "Illustrationen": 0,
    "Noten": 0,
    "Sonstige": 0,
    "Text": 0,
    #"Text$b": 13,
    #"Text$txt": 0,
    "Texto (visual)": 0,
    "aufgefu\u0308hrte Musik": 0,
    #"aufgeführte Musik$b": 0,
    "dreidimensionale Form": 0,
    "dreidimensionales bewegtes Bild": 0,
    "gesprochenes Wort": 0,
    "kartografische dreidimensionale Form": 0,
    "kartografischer Datensatz": 0,
    "kartografisches Bild": 0,
    "kartografisches bewegtes Bild": 0,
    #"nicht spezifiziert": 286,
    #"st": 0,
    #"sti": 11,
    #"still image": 0,
    "taktile dreidimensionale Form": 0,
    "taktiler Text": 0,
    "taktiles Bild": 0,
    #"text": 9,
    #"text$2": 1,
    #"txt": 0,
    #"unbewegtes Bil": 0,
    "unbewegtes Bild": 0,
    #"unbewegtes Bild$b": 0,
    "zweidimensionales bewegtes Bild": 0
}

with open('data/bib-records.json') as f:
    for line in f:
        entry = json.loads(line)
        #   2.271.910 ['002C'] Inhaltsform
        j = 0
        for i in seq_iter(entry):
            j += 1

        if j > 2:
            # 002C Inhaltsform
            inhalt = ''
            try:
                entry['002C']
            except KeyError:
                pass
            else:
                for inh in entry['002C']:
                    try:
                        content[inh['a']]
                    except KeyError:
                        pass
                    else:
                        content[inh['a']] += 1

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()

print('\n \n finished loading dataset')
with open('export/content.json', mode='w') as fi:
    fi.write(json.dumps(content, indent='\t', sort_keys='true'))
