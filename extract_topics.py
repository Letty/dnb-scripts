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
topics = {}

with open('export/bib-records-reduced.json') as f:
    for line in f:
        entry = json.loads(line)

        # Topics
        #   768.701 ['044F'] Schlagwörter aus Altdaten der Deutschen
        # Nationalbibliothek
        #   143.756 ['044H'] Automatisch vergegebenes Schlagwort
        #   259.970 ['044K'] GND-Schlagwörter
        # 4.350.351 ['044N'] Deskriptoren aus einem Thesaurus
        # 1.066.192 ['045C'] 2. + 3.maschinell vergebene Sachgruppen
        # 4.647.455 ['045E'] Sachgruppen der Deutschen Nationalbibliografie
        #   110.813 ['045G'] DDC-Notation: Vollständige Notation
        # 2.621.471 ['041A']      1.Schlagwortfolge 1.Element
        # 2.355.042 ['041A/01']   1.Schlagwortfolge 2.Element
        # 1.556.937 ['041A/02']   1.Schlagwortfolge 3.Element
        #   870.757 ['041A/03']   1.Schlagwortfolge 4.Element
        # 1.752.704 ['041A/08']  Vorgegebene(s) Permutationsmuster zur 1. Schlagwortfolge
        # 2.625.849 ['041A/09']  Angaben zur 1. Schlagwortfolge

        # temporäre Datenstruktur für Themen, damit keine Doppelaufführung
        # stattfindet
        current_topics = []

        util.checkField(entry, '044N', ['a'], current_topics)
        util.checkField(entry, '044H', ['a'], current_topics)
        util.checkField(entry, '044K', ['a'], current_topics)
        util.checkField(entry, '045G', ['a'], current_topics)
        util.checkField(entry, '044F', ['a', 'f'], current_topics)
        util.checkField(entry, '045C', ['f', 'g'], current_topics)
        util.checkField(entry, '045E', ['e', 'h'], current_topics)

        util.findKeywords(current_topics, entry, '041A')
        util.findKeywords(current_topics, entry, '041A/01')
        util.findKeywords(current_topics, entry, '041A/02')
        util.findKeywords(current_topics, entry, '041A/03')
        util.findKeywords(current_topics, entry, '041A/08')
        util.findKeywords(current_topics, entry, '041A/09')

        # Wie geh ich hier mit komischen Abkürzungen um? ggf einfach
        # ignorieren und in Text umwandeln?
        # Die DDC und GND Coding Liste müsste man dafür aufschlüsseln

        for cp in current_topics:
            try:
                topics[cp]
            except KeyError:
                topics[cp] = 1
            else:
                topics[cp] += 1

        uptime = str(datetime.now() - startTime).split('.')[0]
        l += 1
        sys.stdout.write('\033[K\033[1;1H')  # cleans line
        sys.stdout.write(
            'File processing %s %ss %s  proccessed lines %i' % (bcolors.OKBLUE, uptime, bcolors.ENDC, l))
        sys.stdout.flush()

print('\n \n finished loading dataset')

t = {}
for key in seq_iter(topics):
    if topics[key] > 5:
        t[key] = topics[key]


with open('export/topics.json', mode='w') as fi:
    fi.write(json.dumps(t, indent=1, sort_keys=True))
