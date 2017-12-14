# -*- coding: utf-8 -*-
import json

fields = {}


def seq_iter(obj):
    return obj if isinstance(obj, dict) else range(len(obj))


# with open('../data/ts-records.json') as f:
# with open('../data/tp-records.json') as f:
with open('../data/bib-records.json') as f:
    for line in f:
        entry = json.loads(line)
        for i in seq_iter(entry):
            try:
                fields[i]
            except KeyError:
                fields[i] = {'count': 1, 'is_array': '',
                             'array_count': 0, 'ids': {}}
            else:
                fields[i]['count'] = fields[i]['count'] + 1

            ind = 0
            for k in entry[i]:
                for j in seq_iter(k):
                    try:
                        fields[i]['ids'][j]
                    except KeyError:
                        fields[i]['ids'][j] = {
                            'count': 1, 'is_array': '',
                            'array_count': 0
                        }
                    else:
                        fields[i]['ids'][j]['count'] = fields[
                            i]['ids'][j]['count'] + 1

                    jind = 0
                    for l in k:
                        jind += 1
                    if fields[i]['ids'][j]['array_count'] < jind:
                        fields[i]['ids'][j]['array_count'] = jind

                    if fields[i]['ids'][j]['array_count'] > 1:
                        fields[i]['ids'][j]['is_array'] = True
                    else:
                        fields[i]['ids'][j]['is_array'] = False

                ind += 1

            if ind > 1:
                fields[i]['is_array'] = True
            else:
                fields[i]['is_array'] = False

            fields[i]['array_count'] = ind

# with open('keyword_ids.json', mode='w') as fi:
# with open('person_ids.json', mode='w') as fi:
with open('bib_ids.json', mode='w') as fi:
    fi.write(json.dumps(fields, indent='\t', sort_keys='true'))
