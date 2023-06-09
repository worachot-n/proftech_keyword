# -*- coding: utf-8 -*-
# Import libraries
from pythainlp.corpus import (thai_stopwords,
                              thai_words,
                              thai_syllables,
                              thai_family_names,
                              thai_female_names,
                              thai_male_names)
from pythainlp.corpus.ttc import word_freqs
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize
import clean_text


# Word preparation
# Keep words
thaiwords = thai_words()
syllables = thai_syllables()
familyname = thai_family_names()
femalename = thai_female_names()
malename = thai_male_names()

# Remove words
# Thai stop words
stopwords = list(thai_stopwords())
stopwords.append("nan")
stopwords.append("-")
stopwords.append("_")
stopwords.append("")
stopwords.append(" ")

# Thai frequency word
freqswords = word_freqs()
freq = 100  # Set frequency
freqsResults = []

for line in list(freqswords):
    if line[1] >= freq:  # More than threshold means frequency
        freqsResults.append(line[0])


syntax_list = ['', '.', 'ๆ', 'ฯ', '“', '"', "‘", "’",
               "'“", "”'", "\"'", "'‘", "’'", "'", "''", "'“", "”'"]


# Tokenize
def tokenize_word(text, trie):
    text_clean = list(map(clean_text.cleanText_Pandas, text))
    words = []
    for i, text in enumerate(text_clean):
        tokenText = word_tokenize(
            text, engine='newmm', custom_dict=trie, keep_whitespace=False)  # Using 'nercut'
        tokenText = [normalize(word)
                     for word in tokenText]  # Normalization word
        # print(tokenText)
        # Remove Thai stop words
        # tokenText = [word for word in tokenText if not word in stopwords]
        # print(tokenText)
        # Remove Thai frequency words
        tokenText = [word for word in tokenText if not word in freqsResults]
        # Remove space
        tokenText = [
            word for word in tokenText if not word in syntax_list]
        # print(tokenText)
        # tokenText = [word for word in tokenText if not word in manual_word] #Remove Thai frequency words
        # Keep Thai word and name
        # tokenText = [
        #     word for word in tokenText if word in thaiwords or word in familyname or word in femalename or word in malename or word in syllables]
        words.append(tokenText)

    return words


# result = tokenize_word(['ชาวเน็ตร่วมติด หลังไม่พอใจ เลื่อนสอบ tcas หลังจากที่วันที่ 7 มี.ค. 2564 เพจเฟซบุ๊ก mytcas.com ได้ออกเอกสารประกาศว่าจะไม่มีการเลื่อนสอบ สอบความถนัดทั่วไป gat สอบความถนัดทางวิชาการวิชาชีพ pat สอบทางการศึกษาขั้นพื้นฐานแห่งชาติ onet และการสอบ 9 วิชาสามัญดราม่าทวีตเตอร์โดยระบุว่า กระทรวงศึก…หลังจากที่วันที่ 7 มี.ค. 2564 เพจเฟซบุ๊ก mytcas.com ได้ออกเอกสารประกาศว่าจะไม่มีการเลื่อนสอบ สอบความถนัดทั่วไป gat สอบความถนัดทางวิชาการวิชาชีพ pat สอบทางการศึกษาขั้นพื้นฐานแห่งชาติ onet และการสอบ 9 วิชาสามัญดราม่าทวีตเตอร์โดยระบุว่า กระทรวงศึกษาธิการ ร่วมกับที่ประชุมอธิการบดีแห่งประเทศไทย กลุ่มสถาบันแพทยศาสตร์แห่งประเทศไทย สำนักงานคณะกรรมการการศึกษาขั้นพื้นฐาน และสถาบันทดสอบทางการศึกษาแห่งชาติ องค์การมหาชน เรื่อง ข้อเรียกร้องการเลื่อนสอบรายวิชาที่ใช้ในระบบการคัดเลือกกลางบุคคลเข้าศึกษาในสถาบันอุดมศึกษา ปีการศึกษา 2564 tcas64 โดยมติประชุมมีมติร่วมกันว่า ไม่ควรให้มีการเลื่อนสอบ พร้อมกับให้เหตุผล 10 ข้อ หากมีการเลื่อนสอบจะส่งผลกระทบกับผู้ที่มีความพร้อมและประสงค์จะสอบในวันและเวลาเดิม รวมไปถึงกระทบต่อการสอบคัดเลือกอื่นๆแถลงการณ์ไม่เลือนสอบแถลงการณ์ไม่เลือนสอบหลังจากที่การประกาศออกมาไม่นาน ในโซเชียลมิวายมีดราม่า ทวิตเตอร์ร้อนระอุ วิพากษ์วิจารณ์และตั้งข้อสังเกตถึงการตัดสินใจดังกล่าว พร้อมติดแฮชแท็ค ซึ่งเกิดเสียงวิพากวิจารณ์ต่างๆนาๆว่า สนามสอบอยู่ในพื้นที่เสี่ยง และวันสอบ gatpat ในปี 2564 หลายโรงเรียนตรงกับวันสอบปลายภาค เด็กไม่สามารถเลือกไปสอบได้ เพราะเป็นการสอบที่สำคัญทั้งคู่ ขณะที่วันสอบ 9 วิชาสามัญ ตรงกับวันเกณฑ์ทหาร และตรงกับวันสอบของมหาวิทยาลัยสำหรับเด็กที่ต้องการซิ่วดราม่าทวีตเตอร์แถมช่วงที่ผ่านมาบางโรงเรียนเพิ่งเปิดเทอม เด็กยังเรียนไม่เต็มที่ ไม่เข้าใจเนื้อหาเต็มที่ ซึ่งแฮชแท็ค พุ่งติดเทรนด์ทวิตฯอันดับ1 ในระยะเวลาหนึ่งเอาเป็นว่าต้องลุ้นกันต่อว่า ปัญหานี้จะได้รับการแก้ไขอย่างไร',
#                         'กองทัพเรือ ยืนยัน ล่าสุด กรณีกำลังพล เรือหลวงสุโขทัย วันนี้พบ 6 ศพ แต่มีหลักฐานบ่งชี้ว่าเป็นกำลังพล 5 นาย เร่งพิสูจน์อัตลักษณ์ รวมสูญหาย 17 นาย'])
# print(result)
