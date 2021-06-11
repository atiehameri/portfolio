##### Writer : "Atia"



##### Importing Libraries
import nltk
import pandas as pd
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_columns', 800)
from nltk.stem.porter import *
import os
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()


os.chdir("/Users/macbook/Documents/pyhton/portfolio/Keyword_Frequency")

##### reading the file
path = "clean_data_ready_for_count.xlsx"
df = pd.read_excel(path)

df.columns = ["number", "city", "page", "source", "text"]
d = df[["city", "source", "text"]]
d = d.dropna()
data = d.values.tolist()

city_list = df["city"].unique()
source_list = ['Personal Blogs', 'Third Party Websites', 'Official Websites']

total_data = []

text = []
for i in data:
    te = i[2]
    text.append(te)


s = " ".join(text)
words = nltk.tokenize.word_tokenize(s)

freq = nltk.FreqDist(words)
list = freq.most_common(2000)

df = pd.DataFrame(list)
df.to_excel("2000words.xlsx")