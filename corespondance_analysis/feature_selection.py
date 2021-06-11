##### writer "Atia"

##### importing the Libraries
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import prince # for multiple correspondence analysis
from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()
##### Setting Pandas Options
pd.set_option('display.max_rows', 200)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_columns', 800)

os.chdir("/Users/macbook/Documents/pyhton/portfolio/corespondance_analysis")

##### Read the File
path = "all_words_source.xlsx"
d2 = pd.read_excel(path)



##### Select two Columns and save for furthure analysis
d = d2[["source", "word"]]
# dir =  "/Users/macbook/Documents/PhD/2020pyhton/Text_analysis_Final/CA_analysis/for_each_source"
name = ("excel_for_JMP overall CA for JMP.xlsx" )
# name = os.path.join(dir, fname)
if os.path.exists(name):
    os.remove(name)
d.to_excel(name)


##### Make a Pivote Table
tab2 = pd.pivot_table(d, index="source", columns="word", aggfunc=len)

##### Fill the empty spaces with with value Zero
tab2 = tab2.fillna(0)


##### Correspondance analysis with Princ Library
ca = prince.CA(
    n_components=2,
    n_iter=3,
    copy=True,
    check_input=True,
    engine='auto',
    random_state=42,
)

ca = ca.fit(tab2)
eigenvalues = (ca.eigenvalues_)
total_inertia = (ca.total_inertia_)
explained_inertia = (ca.explained_inertia_)
i1 = round(explained_inertia[0], 2)
i2 = round(explained_inertia[1], 2)


##### Saving the reuslt in Excel Format
title = ["Dimension", "Singular Values", "Total Inertia", "Explained Inertia", "Cumulative Inertia"]
row1 = ["Dimension1",eigenvalues[0], " " , explained_inertia[0],explained_inertia[0]*100 ]
row2 = ["Dimension2",eigenvalues[1], total_inertia, explained_inertia[1],
        (explained_inertia[0]+explained_inertia[1])*100]
print(row1)
print(row2)

word = pd.read_excel("/Users/macbook/Documents/PhD/2020pyhton/Text_analysis_Final/factor_analysis/factor_overexcel_file-150.xlsx")
word.columns = ["a", "b", "word"]

factor_list = word["word"].to_list()
print(len(factor_list))


##### Print plot options was limited so I used the x&y data to plot them manually
#### with scatter plot
v = ca.row_coordinates(tab2)
v['index'] = v.index
f = ca.column_coordinates(tab2)
f['index'] = f.index

f = f[f["index"].isin (factor_list)]
Sources = [v[0].tolist(), v[1].tolist(), v["index"].tolist()]
Attributes = [f[0].tolist(), f[1].tolist(), f["index"].tolist()]

plt.rcParams['font.family'] = "sans-serif"

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

ax.scatter(Sources[0], Sources[1], c='#f68b37', marker="o", s=15)
ax.scatter(Attributes[0], Attributes[1], c="#735698", marker="o", s=9)

# Add the names as text labels for each point
for x_pos, y_pos, label in zip(v[0].tolist(), v[1].tolist(), v["index"].tolist()):
    ax.annotate(label,  # The label for this point
                xy=(x_pos, y_pos),  # Position of the corresponding point
                xytext=(5, 2),  # Offset text by 7 points to the right
                textcoords='offset points',  # tell it to use offset points
                ha='left',  # Horizontally aligned to the left
                va='center',
                fontsize=10)  # Vertical alignment is centered

# Add the participant names as text labels for each point
for x_pos, y_pos, label in zip(f[0].tolist(), f[1].tolist(), f["index"].tolist()):
    ax.annotate(label,  # The label for this point
                xy=(x_pos, y_pos),  # Position of the corresponding point
                xytext=(5, 2),  # Offset text by 7 points to the right
                textcoords='offset points',  # tell it to use offset points
                ha='left',  # Horizontally aligned to the left
                va='center',
                fontsize=7)  # Vertical alignment is centered

ax.xaxis.set_ticks(np.arange(-1, 1.1, .25))
ax.tick_params(axis='both', which='major', labelsize=7)

# ax1.f.plot.scatter(x = 0, y = 1, label='Dimensions', c='b', marker="o")
plt.legend(loc='upper left')

##### Ajusting the legend
ax.legend(prop={"size": 7}, borderpad=.5, labelspacing=1, labels=['Data Source', 'Attributes'])
plt.plot([0, 0], [-1, 1], linewidth=.5, color="Black")
plt.plot([-1, 1], [0, 0], linewidth=.5, color="Black")

plt.xlim(-.8, 0.8)
plt.ylim(-.8, 0.8)

plt.xlabel('Dimension One, %s Inertia' % i1, fontsize=8)
plt.ylabel('Dimension Two %s Inertia' % i2, fontsize=8)

### Setting the grid
ax.xaxis.grid(linewidth=.3)
ax.yaxis.grid(linewidth=.3)

### Setting the title
ax.set_title("Correspondence Analysis of All Data" , fontsize=10)


##### saving the image with high resoloution
name2 = ("overall_CA.png" )
plt.savefig("Conceptual_map.png", dpi= 320)
