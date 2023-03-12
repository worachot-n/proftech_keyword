# Import libraries
import pandas as pd
import numpy as np
import re
import string
import matplotlib as mpl
import matplotlib.pyplot as plt

from pythainlp.corpus import (thai_stopwords,
                              thai_words,
                              thai_syllables,
                              thai_family_names,
                              thai_female_names,
                              thai_male_names)
from pythainlp.corpus.ttc import word_freqs
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize
from pythainlp.util import dict_trie
from pythainlp import Tokenizer
from pythainlp.tag import pos_tag, pos_tag_sents
import configure as conf
from tokenize_word import tokenize_word, hashtag_keyword


# words = ['ชาวเน็ตร่วมติด หลังไม่พอใจ เลื่อนสอบ tcas หลังจากที่วันที่ 7 มี.ค. 2564 เพจเฟซบุ๊ก mytcas.com ได้ออกเอกสารประกาศว่าจะไม่มีการเลื่อนสอบ สอบความถนัดทั่วไป gat สอบความถนัดทางวิชาการวิชาชีพ pat สอบทางการศึกษาขั้นพื้นฐานแห่งชาติ onet และการสอบ 9 วิชาสามัญดราม่าทวีตเตอร์โดยระบุว่า กระทรวงศึก…หลังจากที่วันที่ 7 มี.ค. 2564 เพจเฟซบุ๊ก mytcas.com ได้ออกเอกสารประกาศว่าจะไม่มีการเลื่อนสอบ สอบความถนัดทั่วไป gat สอบความถนัดทางวิชาการวิชาชีพ pat สอบทางการศึกษาขั้นพื้นฐานแห่งชาติ onet และการสอบ 9 วิชาสามัญดราม่าทวีตเตอร์โดยระบุว่า กระทรวงศึกษาธิการ ร่วมกับที่ประชุมอธิการบดีแห่งประเทศไทย กลุ่มสถาบันแพทยศาสตร์แห่งประเทศไทย สำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน และสถาบันทดสอบทางการศึกษาแห่งชาติ องค์การมหาชน เรื่อง ข้อเรียกร้องการเลื่อนสอบรายวิชาที่ใช้ในระบบการคัดเลือกกลางบุคคลเข้าศึกษาในสถาบันอุดมศึกษา ปีการศึกษา 2564 tcas64 โดยมติประชุมมีมติร่วมกันว่า ไม่ควรให้มีการเลื่อนสอบ พร้อมกับให้เหตุผล 10 ข้อ หากมีการเลื่อนสอบจะส่งผลกระทบกับผู้ที่มีความพร้อมและประสงค์จะสอบในวันและเวลาเดิม รวมไปถึงกระทบต่อการสอบคัดเลือกอื่นๆแถลงการณ์ไม่เลือนสอบแถลงการณ์ไม่เลือนสอบหลังจากที่การประกาศออกมาไม่นาน ในโซเชียลมิวายมีดราม่า ทวิตเตอร์ร้อนระอุ วิพากษ์วิจารณ์และตั้งข้อสังเกตถึงการตัดสินใจดังกล่าว พร้อมติดแฮชแท็ค ซึ่งเกิดเสียงวิพากวิจารณ์ต่างๆนาๆว่า สนามสอบอยู่ในพื้นที่เสี่ยง และวันสอบ gatpat ในปี 2564 หลายโรงเรียนตรงกับวันสอบปลายภาค เด็กไม่สามารถเลือกไปสอบได้ เพราะเป็นการสอบที่สำคัญทั้งคู่ ขณะที่วันสอบ 9 วิชาสามัญ ตรงกับวันเกณฑ์ทหาร และตรงกับวันสอบของมหาวิทยาลัยสำหรับเด็กที่ต้องการซิ่วดราม่าทวีตเตอร์แถมช่วงที่ผ่านมาบางโรงเรียนเพิ่งเปิดเทอม เด็กยังเรียนไม่เต็มที่ ไม่เข้าใจเนื้อหาเต็มที่ ซึ่งแฮชแท็ค พุ่งติดเทรนด์ทวิตฯอันดับ1 ในระยะเวลาหนึ่งเอาเป็นว่าต้องลุ้นกันต่อว่า ปัญหานี้จะได้รับการแก้ไขอย่างไร',
#          'ฮือฮา!ฝนถล่มลูกเห็บตกกลางกรุง แห่แชะรูปแชร์เฟซ']


def find_word(content_list):
    # ai_oganic_news = model.predict_fake(content_list)
    words_list = tokenize_word(content_list)
    tag_word = pos_tag_sents(words_list)
    words_NCMN = [[(element[0]) for element in sub_arr if element[1] == 'NCMN']
                  for sub_arr in tag_word]
    # words = [[(element[0]) for element in sub_arr]
    #          for sub_arr in tag_word]
    # print(words_NCMN)

    bag_word = hashtag_keyword()
    # print(bag_word)

    tag_list = list(bag_word)
    tag_pos = pos_tag(tag_list)
    # print(tag_pos)
    filtered_tag = [(element[0])
                    for element in tag_pos if element[1] == 'NCMN']
    # print(filtered_tag)

    # filtered_tag.remove('อ.')
    filtered_tag_set = set(filtered_tag)
    result = [[word for word in sublist if any(
        word == w for w in filtered_tag_set)] for sublist in words_NCMN]

    keyword = [
        [word for word in set(sublist)] for sublist in result]

    for i, text_list in enumerate(keyword):
        if len(text_list) <= 5:
            set1 = set(words_NCMN[i])
            list1 = [sorted(set1, key=lambda x: len(x), reverse=True)]
            select = 10-len(text_list)
            print(list1[0][:select])
            keyword[i].extend(list1[0][:select])

    return words_NCMN, keyword


# w, k = find_word(words)
# print(w)
# print('========================')
# print(k)
