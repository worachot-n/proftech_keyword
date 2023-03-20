import dbx as db
import model_predict as model
import time
import datetime
import csv
import configure as conf
import select_word_keyword
import connectdb
import configures as confs
from pythainlp.corpus import thai_words
from pythainlp.util import dict_trie
import clean_text


path = conf.path


# Batch_size = int(sys.argv[1])
# print('Batch_size',Batch_size)
# Batch_size = 100   #-----------------------------
Batch_size = conf.batch_size

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


def update_db_list(id, ai_dc, ai_sp, ai_hc, ai_ml, ai_hm, ai_words, ai_keywords):
    V = []
    print(len(id))
    print(len(ai_dc))
    sql = "UPDATE newsai SET ai2_digital_culture=%s, ai2_soft_power=%s, ai2_healthcare=%s, \
    ai2_make_a_living=%s, ai2_harmony=%s, ai2_list_word=%s, ai2_noun=%s where id=%s"
    for i in range(len(id)):
        val = (ai_dc[i], ai_sp[i], ai_hc[i], ai_ml[i],
               ai_hm[i], ai_words[i], ai_keywords[i], id[i])
        V.append(val)
    print(V)
    xcount = db.updatepara_multi(sql, V)
    print(xcount, "record updated.")


# sqlx="SELECT id,news_title,news_content FROM newsai ORDER BY id desc "
# sqlx = "SELECT id, news_title, news_content FROM newsai WHERE ai2_digital_culture IS NULL ORDER BY id DESC"
sqlx = "SELECT id, news_title, news_content FROM newsai WHERE ai2_digital_culture IS NOT NULL ORDER BY id DESC"
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
        content_list, bag_word_db, trie)
    ai_words = [', '.join(inner_list) for inner_list in ai_words_list]
    ai_keywords = [', '.join(inner_list) for inner_list in ai_keywords_list]

    # update_db_list(ID, ai_dc, ai_sp, ai_hc, ai_ml,
    #                ai_hm, ai_words, ai_keywords)
    print("=====================================")
    print(ai_words)
    print(ai_keywords)
    print(ai_dc, ai_sp, ai_hc, ai_ml, ai_hm)
    print("=====================================")

    print('-'*10)
    print(i, time.time()-t, datetime.datetime.now(), ID)
    with open(path+'log.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([i, time.time()-t, datetime.datetime.now()])
    i += 1
    t = time.time()
