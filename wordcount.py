from wordcloud import WordCloud  # ใช้ทำ Word Cloud
import matplotlib.pyplot as plt  # ใช้ในการแสดง Word Cloud
import dbx as db

# ai2_digital_culture = 1 เลือก domain digital culture และวันที่ '2023-03-28' ถึง '2023-03-29'
sqlx = "SELECT ai2_list_word FROM newsai WHERE ai2_digital_culture = 1 AND news_date >= '2023-03-28' AND news_date <= '2023-03-29'"
myresult = db.query(sqlx)
# print(len(myresult))
merged_list = []
for sublist in myresult:
    merged_list.extend(sublist[0].split(', '))

# print(merged_list)
# print(len(merged_list))


word_string = ' '.join(merged_list)

# Generate the word cloud
wordcloud = WordCloud(font_path='THSarabunNew.ttf', width=800, height=400,
                      background_color='white', regexp=r"[\u0E00-\u0E7Fa-zA-Z']+").generate(word_string)

# Display the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
