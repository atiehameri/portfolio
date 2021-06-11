#### Writer Atieh Ameri

##### Import Library
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, chi2 # for chi-squared feature selection
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_columns', 800)
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()

os.chdir("/Users/macbook/Documents/pyhton/portfolio/Keyword_Frequency/Feature_Selection")


#### read the file
path = "addedone.xlsx"
d2 = pd.read_excel(path)
d = d2[["source", "word"]]


df = pd.get_dummies(d, drop_first=False)
clist = df.columns.to_list()
n= []
for i in clist :
    l = i.split("_")
    i = l[1]
    n.append(i)
df.columns= n


d1 = df.drop(['A','B', 'C'] , axis=1)  # input categorical features
d2 = df[['A','B', 'C']]  # target variable

# categorical feature selection
sf = SelectKBest(chi2, k="all")
sf_fit = sf.fit(d1, d2)

features = []
for i in range(len(sf_fit.scores_)):
    g =[sf_fit.scores_[i],d1.columns[i] ]
    features.append(g)

features.sort(reverse=True)
list=[]
for i in range(60):
   list.append(features[i])



datset = pd.DataFrame(list)
datset.columns = ["score", "word"]
datset['feature'] =datset["word"]
datset['scores'] = datset["score"]
datset = datset.sort_values(by='scores', ascending=True)



####plottingit
plt.rcParams['font.family'] = "sans-serif"
plt.figure(figsize=(12,14))
ax = sns.barplot(datset['scores'], datset['feature'], color ="#735698", alpha= 0.6, label='small',  capsize = 0.06)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=6)
ax.set_xticklabels(ax.get_xticks(), size = 6)
plt.ylabel('Keywords', fontsize=10)
plt.xlabel('Score', fontsize=10)
plt.subplots_adjust(  hspace=.6,bottom=.21 , left= .18 )



name = "text_oveall_factoranalysis_60.png"
if os.path.exists(name):
    os.remove(name)
plt.savefig(name, dpi = 200)
