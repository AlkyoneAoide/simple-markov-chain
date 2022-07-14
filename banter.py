# monte carlo markov chain experiment

import sys
import random

# if first arg isnt a number, quit
if type(int(sys.argv[1])) != int:
    print("first arg should be int")
    exit()

if len(sys.argv) < 3:
    print("need > 1 arg")
    exit()

# Declare variables
# size = 1st argument = solo, pair, tri, etc. group
size = int(sys.argv[1])
# text = text to learn from
text = ""
# ngram = set of all word pairings and their valid choices
ngram = {}

word_list = []

# read all other args as files into the text variable
for f in sys.argv[2:]:
    file = open(f, 'r')
    text += file.read() + "\n"
    file.close()

# strip bad characters from text
text = text.lower().replace('"',' ').replace("'",' ').replace('\n',' ').replace(')',' ').replace('(',' ').replace('[',' ').replace(']',' ').replace('’',' ').replace("“",' ').replace("”",' ')

for sentence in text.split('.'):
    for i in range(1, len(sentence.split(' ')) - (size - 2)):
        for j in range(size):
            word_list.append(sentence.split(' ')[i + j - 1])
        if '' in word_list:
            word_list = []
            continue
        if (tuple(word_list)) not in ngram:
            ngram[tuple(word_list)] = []
        try:
            ngram[tuple(word_list)].append(sentence.split(' ')[i + size - 1])
        except IndexError:
            ngram.pop(tuple(word_list))
            continue
        word_list = []

# print(ngram)
word_list = list(random.choice(list(ngram.keys())))
out = word_list[0] + ' '
for i in range (1, size):
    out += word_list[i] + ' '

while True:
    if tuple(word_list) not in ngram:
        break
    third = random.choice(ngram[tuple(word_list)])
    out += third + ' '
    word_list.append(third)
    new_list = []
    for i in range (size):
        new_list.append(word_list[-(i+1)])
    new_list.reverse()
    word_list = new_list

print ('output banter: \n', out)
