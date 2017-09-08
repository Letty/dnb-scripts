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


def checkField(data, id, subfields, array):
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
                    for tj in ti[i]:
                        # if tj[0] == '\"' or tj[0] == ' ':
                        #     break

                        checkArray(array, tj)


def checkArray(array, value):
    try:
        array.index(value)
    except ValueError:
        array.append(value)
