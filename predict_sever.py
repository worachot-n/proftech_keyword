import configure as conf
import dbx as db
import model_predict as model
import time
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
import sys
import datetime
import csv
import configure as conf
import select_word_keyword

path = conf.path

# Batch_size = int(sys.argv[1])
# print('Batch_size',Batch_size)
# Batch_size = 100   #-----------------------------
Batch_size = conf.batch_size


def update_db_list(id, ai_dc, ai_sp, ai_hc, ai_ml, ai_hm, ai_words, ai_keywords):
    V = []
    print(len(id))
    print(len(ai_dc))
    for i in range(len(id)):
        sql = "UPDATE newsai SET ai2_digital_culture=%s, ai2_soft_power=%s, ai2_healthcare=%s, \
            ai2_make_a_living=%s, ai2_harmony=%s, ai2_list_word=%s, ai2_noun=%s where id=%s"
        val = (ai_dc[i], ai_sp[i], ai_hc[i], ai_ml[i],
               ai_hm[i], ai_words[i], ai_keywords[i], id[i])
        V.append(val)
    print(V)
    xcount = db.updatepara_multi(sql, V)
    print(xcount, "record updated.")


# sqlx="SELECT id,news_title,news_content FROM newsai ORDER BY id desc "
# sqlx = "SELECT id, news_title, news_content FROM newsai WHERE ai2_digital_culture IS NULL ORDER BY id DESC"
sqlx = "SELECT id, news_title, news_content FROM newsai ORDER BY id DESC"
myresult = db.query(sqlx)
print('Total Data unlabeled', len(myresult))

i = 0
t = time.time()
while myresult:
    b = []
    if len(myresult) < Batch_size:
        Batch_size = len(myresult)
    for i in range(Batch_size):
        b.append(myresult.pop(0))

    ID = []
    content_list = []
    for x in b:
        ID.append(str(x[0]))
        content_list.append(str(x[1]))
    print(len(content_list))
    ai_dc = model.predict_dc(content_list)
    ai_sp = model.predict_sp(content_list)
    ai_hc = model.predict_hc(content_list)
    ai_ml = model.predict_ml(content_list)
    ai_hm = model.predict_hm(content_list)
    ai_words_list, ai_keywords_list = select_word_keyword.find_word(
        content_list)
    ai_words = [', '.join(inner_list) for inner_list in ai_words_list]
    ai_keywords = [', '.join(inner_list) for inner_list in ai_keywords_list]

    update_db_list(ID, ai_dc, ai_sp, ai_hc, ai_ml,
                   ai_hm, ai_words, ai_keywords)

    print('-'*10)
    print(i, time.time()-t, datetime.datetime.now(), ID)
    with open(path+'log.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, time.time()-t, datetime.datetime.now()])
    i += 1
    t = time.time()
