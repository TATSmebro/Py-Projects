sentence = input()
key = input()
alphabet = 'abcdefghijklmnopqrstuvwxyz'

table = list(key)

for i in sentence:
    if i in alphabet:
        print(table[alphabet.index(i)], end='')
    else:
        print(i, end='')