unicode = open('unicode.txt', 'r', encoding="UTF-8").read().split(' ')
legacy = open('legacy.txt', 'r', encoding="UTF-8").read().split(' ')
legacy_isi = open('isi font legacy.txt', 'r', encoding="UTF-8").read().split(' ')


def uni2fm(user_input=None):
    replaced = user_input
    for i in range(len(unicode)):
        if unicode[i] in user_input:
            replaced = replaced.replace(unicode[i], legacy[i])
    u = user_input.split()
    r = replaced.split()
    for j in range(len(u)):
        if u[j] == r[j]:
            replaced = replaced.replace(u[j],"^"+u[j]+"&")
    replaced = replaced.replace("a‍r", "%")
    return replaced


def uni2isi(user_input=None):
    replaced = user_input
    for i in range(len(unicode)):
        if unicode[i] in user_input:
            replaced = replaced.replace(unicode[i], legacy_isi[i])
    u = user_input.split()
    r = replaced.split()
    for j in range(len(u)):
        if u[j] == r[j]:
            replaced = replaced.replace(u[j],"("+u[j]+")")
    replaced = replaced.replace("Š‍y", "±")
    return replaced
