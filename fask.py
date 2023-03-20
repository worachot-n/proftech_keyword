import select_word_keyword
import configure as conf
from thai2transformers.preprocess import process_transformers
import sys
import torch.nn.functional as F
import torch
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
from flask import Flask, jsonify, make_response
import select_word_keyword
import connectdb
import configures as confs
from pythainlp.corpus import thai_words
from pythainlp.util import dict_trie
import clean_text


app = Flask(__name__)

# import configure as conf
# import dbx as db

MAX_LENGTH = 416

path = conf.path

param = confs

dbs = connectdb.connection[param.DB_NAME]
# print(db.list_collection_names())
hashtag_db = dbs.hashtag_list.find()
keywords_db = dbs.object.find()


def hashtag_keyword():
    hashtag = hashtag_db
    hashtag = [x for x in hashtag]
    hashtag_list = [sublist['uid'] for sublist in hashtag]
    hashtag_clean = list(map(clean_text.cleanText_Pandas, hashtag_list))
    # print(len(hashtag_clean))

    keywords = keywords_db
    keywords = [x for x in keywords]
    keywords_list = [
        item for sublist in keywords for item in sublist['keywords']]
    keywords_clean = list(map(clean_text.cleanText_Pandas, keywords_list))
    # print(len(keywords_clean))

    hashtags_set = set(hashtag_clean)
    keywords_set = set(keywords_clean)
    bag_word = hashtags_set.union(keywords_set)
    # print(len(bag_word))
    return bag_word


bag_word_db = hashtag_keyword()

# add multiple words
custom_words_list = set(thai_words())
custom_words_list.update(bag_word_db)
trie = dict_trie(dict_source=custom_words_list)

model_dc = AutoModelForSequenceClassification.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_digital_culture/')
tokenizer_dc = AutoTokenizer.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_digital_culture/')
model_sp = AutoModelForSequenceClassification.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_soft_power/')
tokenizer_sp = AutoTokenizer.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_soft_power/')
model_hc = AutoModelForSequenceClassification.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_health_care/')
tokenizer_hc = AutoTokenizer.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_health_care')
model_ml = AutoModelForSequenceClassification.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_make_a_living/')
tokenizer_ml = AutoTokenizer.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_make_a_living/')
model_hm = AutoModelForSequenceClassification.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_harmony')
tokenizer_hm = AutoTokenizer.from_pretrained(
    path+'protech_model/wisesight_sentiment_wangchanberta_harmony')


def predict_dc(content_list):
    batch_dc = tokenizer_dc(
        content_list, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    class_label = {0: 0, 1: 1}
    with torch.no_grad():
        output_test = model_dc(**batch_dc)
        pred_test = F.softmax(output_test.logits, dim=1)
        labels_dc_num = torch.argmax(pred_test, dim=1)
        labels_dc = [class_label[label] for label in labels_dc_num.numpy()]
        return labels_dc


def predict_sp(content_list):
    batch_sp = tokenizer_sp(
        content_list, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    class_label = {0: 0, 1: 1}
    with torch.no_grad():
        output_test = model_sp(**batch_sp)
        pred_test = F.softmax(output_test.logits, dim=1)
        labels_sp_num = torch.argmax(pred_test, dim=1)
        labels_sp = [class_label[label] for label in labels_sp_num.numpy()]
        return labels_sp


def predict_hc(content_list):
    batch_hc = tokenizer_hc(
        content_list, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    class_label = {0: 0, 1: 1}
    with torch.no_grad():
        output_test = model_hc(**batch_hc)
        pred_test = F.softmax(output_test.logits, dim=1)
        labels_hc_num = torch.argmax(pred_test, dim=1)
        labels_hc = [class_label[label] for label in labels_hc_num.numpy()]
        return labels_hc


def predict_ml(content_list):
    batch_ml = tokenizer_ml(
        content_list, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    class_label = {0: 0, 1: 1}
    with torch.no_grad():
        output_test = model_ml(**batch_ml)
        pred_test = F.softmax(output_test.logits, dim=1)
        labels_ml_num = torch.argmax(pred_test, dim=1)
        labels_ml = [class_label[label] for label in labels_ml_num.numpy()]
        return labels_ml


def predict_hm(content_list):
    batch_hm = tokenizer_hm(
        content_list, padding=True, truncation=True, max_length=MAX_LENGTH, return_tensors="pt")
    class_label = {0: 0, 1: 1}
    with torch.no_grad():
        output_test = model_hm(**batch_hm)
        pred_test = F.softmax(output_test.logits, dim=1)
        labels_hm_num = torch.argmax(pred_test, dim=1)
        labels_hm = [class_label[label] for label in labels_hm_num.numpy()]
        return labels_hm


def preprocess(text):
    if isinstance(text, str):
        text = [text]
    return list(map(process_transformers, text))


##########################################################################################


@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/ai/<name>')
def greet(name):
    # name : type list
    text = preprocess(name)
    ai_dc = predict_dc(text)
    ai_sp = predict_sp(text)
    ai_hc = predict_hc(text)
    ai_ml = predict_ml(text)
    ai_hm = predict_hm(text)
    ai_words_list, ai_keywords_list = select_word_keyword.find_word(
        text, bag_word_db, trie)
    ai_words = [', '.join(inner_list) for inner_list in ai_words_list]
    ai_keywords = [', '.join(inner_list) for inner_list in ai_keywords_list]

    return jsonify(
        {'ai_dc': str(ai_dc[0]),
         'ai_sp': str(ai_sp[0]),
         'ai_hc': str(ai_hc[0]),
         'ai_ml': str(ai_ml[0]),
         'ai_hm': str(ai_hm[0]),
         'ai_words': str(ai_words[0]),
         'ai_keywords': str(ai_keywords[0])
         }
    )


@app.route('/')
def hello():

    return jsonify({'message': 'Please Input for predict'})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5577, ssl_context=(
    #     '/etc/ssl/sslnew/certificate.crt', '/etc/ssl/sslnew/private.key'))
    app.run()
