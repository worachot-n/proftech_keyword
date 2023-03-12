# import configure as conf
# import dbx as db
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import sys
from thai2transformers.preprocess import process_transformers
import configure as conf

MAX_LENGTH = 416

path = conf.path

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
        percen = [max(x) for x in pred_test.tolist()]
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
        percen = [max(x) for x in pred_test.tolist()]
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
        percen = [max(x) for x in pred_test.tolist()]
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
        percen = [max(x) for x in pred_test.tolist()]
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
        percen = [max(x) for x in pred_test.tolist()]
        return labels_hm


def preprocess(text):
    if isinstance(text, str):
        text = [text]
    return list(map(process_transformers, text))


##########################################################################################

# text = 'ทอสอบระบบการทำนายโดเมนจากข่าวสาร./,//'
# # text = ['ทอสอบระบบการทำนายโดเมนจากข่าวสาร./,//','หดิกดิำดิกดิกดิกดิกดิกดิกดิ']

# text = preprocess(text)
# (ai_oganic_news,per_ai_oganic_news) = predict_fake(text)
# (ai_useful_pct,per_ai_useful_pct) = predict_useful(text)
# (ai_opinion_pct,per_ai_opinion_pct) = predict_opinion(text)
# (ai_domain,per_ai_domain) = predict_domain(text)

# print('ai_oganic_news',ai_oganic_news,per_ai_oganic_news)
# print('ai_useful_pct',ai_useful_pct,per_ai_useful_pct)
# print('ai_opinion_pct',ai_opinion_pct,per_ai_opinion_pct)
# print('ai_domain',ai_domain,per_ai_domain)
