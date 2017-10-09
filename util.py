import re


def findKeywords(array, data, id):
    try:
        data[id]
    except KeyError:
        pass
    else:
        for ki in data[id]:
            try:
                ki['a']
            except KeyError:
                pass
            else:
                checkArray(array, ki['a'][0])


def checkField(data, id, subfields, array, lookuptable):
    try:
        data[id]
    except KeyError:
        pass
    else:
        for ti in data[id]:
            for i in subfields:

                try:
                    ti[i]
                except KeyError:
                    pass
                else:
                    if isinstance(ti[i], list):
                        for tj in ti[i]:
                            name = ''
                            if lookuptable:
                                name = lookuptable[tj]
                            checkArray(array, name)

                    else:
                        name = ti[i]
                        if lookuptable:
                            try:
                                name = lookuptable[ti[i]]
                            except KeyError:
                                pass
                        checkArray(array, name)


def checkArray(array, value):
    try:
        array.index(value)
    except ValueError:
        array.append(value)


def extractAuthorName(field):
    name = ''

    try:
        name += field['d']
    except KeyError:
        pass

    try:
        name += ' ' + field['a']
    except KeyError:
        pass

    return name


def getYear(st):
    p = re.findall('(\d{4})', st)
    if (len(p) == 0):
        return 0
    else:
        return int(p[0])


def getAuthorId(entry, fieldId, a_array):
    try:
        entry[fieldId]
    except KeyError:
        pass
    else:
        try:
            entry[fieldId][0]['9']
        except KeyError:
            pass
        else:
            try:
                a_array.append(entry[fieldId][0]['9'].lower())
            except KeyError:
                pass


def seq_iter(obj):
    return obj if isinstance(obj, dict) else range(len(obj))
