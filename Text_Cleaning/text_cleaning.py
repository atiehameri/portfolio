###### Writer : "Atia"


##### importing the Libraries
import csv
import re
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
from gensim.parsing.preprocessing import remove_stopwords
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()
import os


os.chdir("/Users/macbook/Documents/pyhton/portfolio/Keyword_Frequency/Text_Cleaning")
####### reading the csv file
raw_data = []
with open("Raw_Text.csv") as mi:
    reader = csv.reader(mi)
    for line in reader:
        raw_data.append(line)

total_data = []

for x in raw_data:

    text = x[3]
    ##### text is a string here, so we need to clean it
    script = text.split("'")
    for sent in script:
        temp = x[:3]
        sent = re.sub(r"[!”#$%&()*+,-./:;<=>\"\'?@[\]^_`{|}~–’]", " ", sent)
        sent = sent.lower()

        #### removing the numbers
        sent = re.sub(r"\d+", "", sent)

        #### removing the empty spaces
        sent = sent.strip()

        #### removing the the stopwords
        sent = remove_stopwords(sent)
        sent = re.sub(r"'", " ", sent)

        ######removing the apastroph
        sent = re.sub("(’\w+) ?", " ", sent)

        ######Separate teh words
        input_str = word_tokenize(sent)
        singledata = []

        for wo in input_str:
            lemword = Lem.lemmatize(wo)
            pattern = re.compile(r"(.)\1{2,}")
            wo = pattern.sub(r"\1\1", lemword)
            if len(wo) > 1:
                singledata.append(lemword)

        s = " ".join(singledata)
        if s != "":
            temp.append(s)

        if len(temp) > 3:
            total_data.append(temp)


df = pd.DataFrame(total_data)
df.columns = ["city", "page", "source", "text"]
path = "clean_data_ready_for_count.xlsx"

### remove teh file if it already exists
if os.path.exists(path):
    os.remove(path)

df.to_excel(path)



