import re
import string
import emoji_string


def clean_space(sublist):
    return ' '.join(sublist.split())


def clean_link(sublist):
    cleaned_sublist = re.sub(
        r'(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ', sublist)
    return cleaned_sublist


def clean_emoji(sublist):
    cleaned_sublist = re.sub(
        emoji_string.emoji, ' ', sublist)
    return cleaned_sublist


def clean_username(sublist):
    cleaned_sublist = re.sub(
        r'@', ' ', sublist)
    return cleaned_sublist


def clean_hashtag(sublist):
    cleaned_sublist = re.sub(
        r'#', ' ', sublist)
    return cleaned_sublist


def clean_retweet(sublist):
    cleaned_sublist = re.sub(
        r'RT', ' ', sublist)
    return cleaned_sublist


def clean_HTML(sublist):
    # apply the regex substitution to each string in the sublist
    cleaned_sublist = re.sub(
        r'<[^<>]*>', ' ', sublist)
    return cleaned_sublist


def clean_slash(sublist):
    # apply the regex substitution to each string in the sublist
    cleaned_sublist = re.sub(
        r'\r+', ' ', sublist)
    cleaned_sublist = re.sub(
        r'\n+', ' ', cleaned_sublist)
    cleaned_sublist = re.sub(
        r'\t+', ' ', cleaned_sublist)
    cleaned_sublist = re.sub(
        r',', ' ', cleaned_sublist)
    return cleaned_sublist


def clean_strip(sublist):
    return sublist.strip()


def clean_lower(sublist):
    return sublist.lower()


# Define function for text cleansing
def cleanText(text):
    newText = list(map(clean_link, text))  # Remove link
    newText = list(map(clean_emoji, newText))  # Remove emoji
    newText = list(map(clean_username, newText))  # Remove @username
    newText = list(map(clean_hashtag, newText))  # Remove hashtag
    newText = list(map(clean_retweet, newText))  # Remove 'RT' Word from tweet
    newText = list(map(clean_HTML, newText))  # Remove all HTML tag
    newText = list(map(clean_slash, newText))
    newText = list(map(clean_strip, newText))
    newText = list(map(clean_lower, newText))
    newText = list(map(clean_space, newText))
    return newText


# Define function for text cleansing
def cleanText_Pandas(text):
    newText = re.sub(
        r'(?:http|ftp|https)://(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ', text)  # Remove link
    newText = re.sub(emoji_string.emoji, '', newText)  # Remove emoji
    newText = re.sub(r'@', ' ', newText)  # Remove @username
    newText = re.sub(r'#', ' ', newText)  # Remove hashtag
    newText = re.sub(r'RT', ' ', newText)  # Remove 'RT' Word from tweet
    newText = re.sub(r'<[^<>]*>', ' ', newText)  # Remove all HTML tag
    # Remove all excessive space, special characters and new line symbols
    newText = re.sub(r'\r+', ' ', newText)
    # Remove all excessive space, special characters and new line symbols
    newText = re.sub(r'\n+', ' ', newText)
    # Remove all excessive space, special characters and new line symbols
    newText = re.sub(r'\t+', ' ', newText)
    # Remove all excessive space, special characters and new line symbols
    newText = re.sub(r',', ' ', newText)
    newText = ' '.join(newText.split())  # Keep only one white space
    return newText


# result = cleanText(['ชาวเน็ตร่วมติด #dek64กําลังถูกทิ้ง หลังไม่พอใจ',
#                     'ฮือฮา!ฝนถล่มลูกเห็บตกกลางกรุง แห่แชะรูปแชร์เฟซ'])
# print(result)
