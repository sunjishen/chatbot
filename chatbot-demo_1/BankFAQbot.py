import pandas as pd
import numpy as np

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split as tts
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.stem.lancaster import LancasterStemmer


stemmer = LancasterStemmer()
def cleanup(sentence):
    word_tok = nltk.word_tokenize(sentence)
    stemmed_words = [stemmer.stem(w) for w in word_tok]

    return ' '.join(stemmed_words)

le = LE()

tfv = TfidfVectorizer(min_df=1, stop_words='english')

data = pd.read_csv("BankFAQs.csv")
questions = data['Question'].values

X = []
for question in questions:
    X.append(cleanup(question))

tfv.fit(X)
le.fit(data['Class'])

X = tfv.transform(X)
y = le.transform(data['Class'])


trainx, testx, trainy, testy = tts(X, y, test_size=.25, random_state=42)

model = SVC(kernel='linear')
model.fit(trainx, trainy)
print("SVC:", model.score(testx, testy))


def get_max5(arr):
    ixarr = []
    for ix, el in enumerate(arr):
        ixarr.append((el, ix))
    ixarr.sort()

    ixs = []
    for i in ixarr[-5:]:
        ixs.append(i[1])

    return ixs[::-1]
#获取前端的数据，开始匹配
def string_find_fun(voice_text):
    print('deal message:'+voice_text)
    t_usr = tfv.transform([cleanup(voice_text.strip().lower())])
    class_ = le.inverse_transform(model.predict(t_usr))
    questionset = data[data['Class']==class_[0]]

    cos_sims = []
    for question in questionset['Question']:
        sims = cosine_similarity(tfv.transform([question]), t_usr)
        cos_sims.append(sims)
        
    ind = cos_sims.index(max(cos_sims))
    
    return data['Answer'][questionset.index[ind]]

def chat():
    cnt = 0
    print("PRESS Q to QUIT")
    print("TYPE \"DEBUG\" to Display Debugging statements.")
    print("TYPE \"STOP\" to Stop Debugging statements.")
    print("TYPE \"TOP5\" to Display 5 most relevent results")
    print("TYPE \"CONF\" to Display the most confident result")
    print()
    print()
    DEBUG = False
    TOP5 = False

    print("Bot: Hi, Welcome to our bank!")
    while True:
        usr = input("You: ")

        if usr.lower() == 'yes':
            print("Bot: Yes!")
            continue

        if usr.lower() == 'no':
            print("Bot: No?")
            continue

        if usr == 'DEBUG':
            DEBUG = True
            print("Debugging mode on")
            continue

        if usr == 'STOP':
            DEBUG = False
            print("Debugging mode off")
            continue

        if usr == 'Q':
            print("Bot: It was good to be of help.")
            break

        if usr == 'TOP5':
            TOP5 = True
            print("Will display 5 most relevent results now")
            continue

        if usr == 'CONF':
            TOP5 = False
            print("Only the most relevent result will be displayed")
            continue

        t_usr = tfv.transform([cleanup(usr.strip().lower())])
        class_ = le.inverse_transform(model.predict(t_usr))
        questionset = data[data['Class']==class_[0]]

        if DEBUG:
            print("Question classified under category:", class_)
            print("{} Questions belong to this class".format(len(questionset)))

        cos_sims = []
        for question in questionset['Question']:
            sims = cosine_similarity(tfv.transform([question]), t_usr)
            cos_sims.append(sims)
            
        ind = cos_sims.index(max(cos_sims))

        if DEBUG:
            question = questionset["Question"][questionset.index[ind]]
            print("Assuming you asked: {}".format(question))

        if not TOP5:
            print("Bot5:", data['Answer'][questionset.index[ind]])
        else:
            inds = get_max5(cos_sims)
            for ix in inds:
                print("Question: "+data['Question'][questionset.index[ix]])
                print("Answer: "+data['Answer'][questionset.index[ix]])
                print('-'*50)

        print("\n"*2)
        outcome = input("Was this answer helpful? Yes/No: ").lower().strip()
        if outcome == 'yes':
            cnt = 0
        elif outcome == 'no':
            inds = get_max5(cos_sims)
            sugg_choice = input("Bot: Do you want me to suggest you questions ? Yes/No: ").lower()
            if sugg_choice == 'yes':
                q_cnt = 1
                for ix in inds:
                    print(q_cnt,"Question: "+data['Question'][questionset.index[ix]])
                    # print("Answer: "+data['Answer'][questionset.index[ix]])
                    print('-'*50)
                    q_cnt += 1
                num = int(input("Please enter the question number you find most relevant: "))
                print("Bot11: ", data['Answer'][questionset.index[inds[num-1]]])

# 1: Is emergency financial assistance provided under Travel Insurance
# A financial emergency is a situation where the insured loses all or a 
# substantial amount of his/her travel funds due to theft, robbery, mugging or dacoity. 
# Under this benefit the insured is provided with Emergency Cash Assistance up to the limit stated in the Policy. 
# This assistance is provided by the company through a service provider.
# 2: Who do I contact for a claim on the Travel Insurance policy
# 3: What are the eligibility criteria for a Travel Insurance policy
# 4: Question: For how many days can the Travel Insurance policy be extended
# 5: Where can I get the list of hospitals extending the cash facility
# There is no standard list of hospitals. The insured needs to intimate the International SOS immediately on admission 
# so that the cashless facility may be extended by the assistance provider.
# chat()
