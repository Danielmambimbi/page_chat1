import nltk
import spacy
from spacy import language
import os
from nltk.corpus import stopwords
import nltk.tokenize.punkt 
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split,cross_val_score,validation_curve,GridSearchCV,StratifiedKFold
from sklearn.metrics import accuracy_score
from flask import Flask, request,render_template,jsonify
from flask_cors import CORS

# nltk.download('averaged_perceptron_tagger_eng')

x=np.array([
    "bonjour",
    "bonjour comment vas-tu ?",
    "comment vas-tu ?",
    "tu vas bien ?",
    "je vais bien",
    "ça va bien",
    "ça va",
    "salut !",
    "je peux avoir des informations sur votre entreprise",
    "renseigner moi sur votre entreprise",
    "renseigner moi sur vous",
    "tu peux me renseigner sur vous",
    "pourre-je avoir plus des détails sur votre entreprise",
    "au revoir !",
    "je peux faire des commande en ligne",
    "la livraison est inclut"
    ])
y=np.array([    
            "oui bonjour, service clientel\nque puis-je faire pour vous ?",
            "oui bonjour, Je vais bien merçi et vous ?",
            "Je vais bien merçi et vous ?",
            "Je vais bien merçi et vous ?",
            "merçi suis ravis d'apprendre ça\nque puis-je faire pour vous ?",
            "merçi suis ravis d'apprendre ça\nque puis-je faire pour vous ?",
            "merçi suis ravis d'apprendre ça\nque puis-je faire pour vous ?",
            "oui salut, service clientel\nque puis-je faire pour vous ?",
            "oui bien-sûr, avec plaisir\nNous sommes l'entreprise X situer en rdc plus precisement au kongo-centre ville de matadi commune de matadi quartier kikanda n°13\nnous vendros de diffères articles telques: les impremants, les ordinateurs, les fourniture bureautique et bien d'autres",
            "oui bien-sûr, avec plaisir\nNous sommes l'entreprise X situer en rdc plus precisement au kongo-centre ville de matadi commune de matadi quartier kikanda n°13\nnous vendros de diffères articles telques: les impremants, les ordinateurs, les fourniture bureautique et bien d'autres",
            "oui bien-sûr, avec plaisir\nNous sommes l'entreprise X situer en rdc plus precisement au kongo-centre ville de matadi commune de matadi quartier kikanda n°13\nnous vendros de diffères articles telques: les impremants, les ordinateurs, les fourniture bureautique et bien d'autres",
            "oui bien-sûr, avec plaisir\nNous sommes l'entreprise X situer en rdc plus precisement au kongo-centre ville de matadi commune de matadi quartier kikanda n°13\nnous vendros de diffères articles telques: les impremants, les ordinateurs, les fourniture bureautique et bien d'autres",
            "oui bien-sûr, avec plaisir\nNous sommes l'entreprise X situer en rdc plus precisement au kongo-centre ville de matadi commune de matadi quartier kikanda n°13\nnous vendros de diffères articles telques: les impremants, les ordinateurs, les fourniture bureautique et bien d'autres",
            "bye à bientot, c'est fu un plaisir",
            "non désoler nous n'avons pas encore implémenter ce système",
            "non désoler nous n'avons pas encore implémenter ce système"
            ])
# print(x.shape)
# print(y.shape)



def preprocessor(text):
    tab=[]
    for raw_text in text:
        nlp= spacy.load("fr_core_news_sm")
        token_list=nltk.word_tokenize(raw_text)
        token_list2=list(filter(lambda token: nltk.tokenize.punkt.PunktToken(token).is_non_punct, token_list))
        token_list3=[word.lower() for word in token_list2]
        token_list4=list(filter(lambda token: token not in stopwords.words('french'),token_list3))
        stemmer=SnowballStemmer('french')
        token_list5=[stemmer.stem(word) for word in token_list4]
        if token_list5!=[]:
            text=" ".join(token_list5)
            tab.append(text)
    tab=np.array(tab)
    return tab
model=make_pipeline(CountVectorizer(),MultinomialNB())

# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.28,random_state=7)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.28,random_state=7)
x_train_av=x_train
y_train_av=y_train
# x_train=preprocessor(x_train)
# x_test=preprocessor(x_test)
model.fit(x_train,y_train)
print(model.score(x_test,y_test))
# y_pred=model.predict(x_test)
# score=accuracy_score(y_test,y_pred)
# print(f"le score du modèle est de : {score}")
# plt.scatter(x,y,label='Données')
# plt.scatter(x_train,y_train,c='lime',label='Données train après p')
# plt.plot(x_test,y_pred,c='red',label='Données après predict')
# plt.legend()
# plt.show()

def chatbot(message):
    # response=model.predict(preprocessor([message]))
    response=model.predict([message])
    return response[0]
# while True:
#     user_input=input("vous : ")
#     if user_input.lower() in ["quit","exit"]:
#         print("chabot : Au revoir !")
#         break
#     response=chatbot(user_input)
#     print(f"Chatbot : {response}")

# i=1
# j=0.01

# while True:
#     if i==101:
#         break
#     x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.28,random_state=i)
#     # x_train=preprocessor(x_train)
#     # x_test=preprocessor(x_test)
#     model.fit(x_train,y_train)
#     print("i = ",i)
#     print(model.score(x_test,y_test))
#     i=i+1



chat5=Flask(__name__)
CORS(chat5)
# @chat5.errorhandler(404)
# def page_not_found(error):
#     return 'This page does not exist', 404
# @chat5.route('/')
# def home():
#     return render_template('page1.html')

@chat5.route('/chat',methods=["POST"])
# def chat():
#     user_input=request.json.get("message")
#     response=""
#     if user_input.lower()=="bonjour":
#         response="oui, bonjour !"
#     else:
#         response="desole, je ne comprends pas"
#     return jsonify({"response":response})
def chat():
    response=""
    user_input=request.form["message"]
    response=model.predict([user_input])
    response=response[0]
    return response
if __name__=="__main__":
    chat5.run(host='0.0.0.0')
    # chat5.run(debug=True)