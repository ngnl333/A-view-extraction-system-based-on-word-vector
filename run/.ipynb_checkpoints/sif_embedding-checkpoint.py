import sys, numpy
sys.path.append('../src')
import data_io, params, SIF_embedding
from goose3 import Goose
import spacy
from tabulate import tabulate


print("""This program theoretically supports all news URL addresses.
But I have only used BBC News to test.
Please enter a news URL:
(Example: https://www.bbc.co.uk/news/world-asia-china-49303877)
-->""")
s=input()

# input
wordfile = '../data/glove.6B.100d.txt' # word vector file, can be downloaded from GloVe website; it's quite large but you can truncate it and use only say the top 50000 word vectors to save time
weightfile = '../data/enwiki_vocab_min200.txt' # each line is a word and its frequency
weightpara = 1e-3 # the parameter in the SIF weighting scheme, usually in the range [3e-5, 3e-3]
rmpc = 1 # number of principal components to remove in SIF weighting scheme
with open("../data/words_mean_say_30.txt",'r') as f:
    wordsMeanSay = f.readlines()
    for i in range(len(wordsMeanSay)):
        wordsMeanSay[i]=wordsMeanSay[i].rstrip()
# print('wordsMeanSay = ',wordsMeanSay)
g = Goose()
article = g.extract(url=s)
sentences=article.cleaned_text.split('\n\n')##list
# print('sentences = ',sentences)
g.close()


# load word vectors
(words, We) = data_io.getWordmap(wordfile)
# print('load words vector finished')
# load word weights
word2weight = data_io.getWordWeight(weightfile, weightpara) # word2weight['str'] is the weight for the word 'str'
weight4ind = data_io.getWeight(words, word2weight) # weight4ind[i] is the weight for the i-th word
# print('load word weights finished')


def getSIFscore(sentences:list,words,weight4ind,rmpc,We,params,sx:int,sy:int):
    # load sentences
    x, m = data_io.sentences2idx(sentences,words)  # x is the array of word indices, m is the binary mask indicating whether there is a word in that location
    w = data_io.seq2weight(x, m, weight4ind)  # get word weights
    # print('load sentences finished')

    # set parameters
    params = params.params()
    params.rmpc = rmpc
    # get SIF embedding
    embedding = SIF_embedding.SIF_embedding(We, x, w, params)  # embedding[i,:] is the embedding for sentence i

    embeddingSize=len(embedding)
    # print('embeddingSize= ',embeddingSize)

    emb=list()
    for x in range(embeddingSize):
        emb.append(embedding[x, :])

    emb1 = emb[sx]
    emb2 = emb[sy]
    inn = (emb1 * emb2).sum()
    emb1norm = numpy.sqrt((emb1 * emb1).sum())
    emb2norm = numpy.sqrt((emb2 * emb2).sum())
    score = inn / emb1norm / emb2norm

    # print(sentences[sx],'--------',sentences[sy],' = ',score,'\n')
    return score

scoreList=[]
for x in range(len(sentences)-1):
    scoreList.append((getSIFscore(sentences, words, weight4ind, rmpc, We, params, x, x+1),x,x+1))

# print('scoreList = ',scoreList)
# print('scoreList[0][0] = ',scoreList[0][0])
# print('scoreList[1][0] = ',scoreList[1][0])

result=[]
x=0
temp=[]

for i in scoreList:
    # print('i[0] = ',i[0])
    if i[0] > 0 :
        temp.append(i[1])
        temp.append(i[2])
    elif i[0] < 0 :
        # result[x].append(temp)
        temp.append(i[1])
        # print('temp [] = ', temp)

        result.append(sorted(list(set(temp.copy()))))

        temp.clear()
        # print('result = ',result)
        continue
result.append(sorted(list(set(temp.copy()))))


# print('result = ',result)


##查找哪个句子里面有say
index=[]
for i in range(len(sentences)):
    for x in wordsMeanSay:
        if x in sentences[i].split():
            # print('x = ',x,' i = ',i)
            index.append(i)

# print('index = ',index)

indexofblock=[]
for i in index:
    for x in range(len(result)):
        for y in result[x]:
            if int(i)==int(y):
                indexofblock.append(x)
indexofblock=sorted(list(set(indexofblock)))
# print('indexofblock = ',indexofblock)

sentencesBlock=[]
tempBlock=[]
for i in indexofblock:
    for x in result[i]:
        tempBlock.append(sentences[x])
    # print('tempBlock = ',tempBlock)
    sentencesBlock.append(tempBlock.copy())
    tempBlock.clear()


for i in range(len(sentencesBlock)):
    sentencesBlock[i] = ''.join(sentencesBlock[i])

# print('sentencesBlock = ',sentencesBlock)

nlp = spacy.load("en_core_web_sm")
templabel=[]
label=[]
for i in range(len(sentencesBlock)):
    doc = nlp(sentencesBlock[i])
    for ent in doc.ents:
        # print(ent.text, ent.label_)
        temp=[ent.text, ent.label_]
        templabel.append(temp)
    label.append(templabel.copy())
    templabel.clear()
# print('label = ',label)


temprow=[]
temprow2=[]
rows=[]
for i in range(len(label)):
    for x in range(len(label[i])):
        if label[i][x][1] == 'ORG':
            temprow.append(label[i][x][0])
        elif label[i][x][1] == 'PERSON':
            temprow.append(label[i][x][0])
        # else: temprow.append('')
    temprow2.append(' , '.join(temprow))
    temprow2.append(sentencesBlock[i])
    rows.append(temprow2.copy())
    temprow.clear()
    temprow2.clear()
# print('rows = \n',rows)

print(tabulate(rows, headers=['Person / Org','View'], tablefmt="fancy_grid"))


