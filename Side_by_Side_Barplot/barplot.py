#### Writer "Atia"


#### Importing the library
import os
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 20)

os.chdir("/Users/macbook/Documents/pyhton/portfolio/Side_by_Side_Barplot")
##### Reading the file
rpath = "renamed.xlsx"
df2 = pd.read_excel(rpath)

#### select required columns
tab = pd.pivot_table(df2, index=['source'], columns= ["new_tag"], aggfunc= len)

print(tab)



##### have a sum
tab ["sum"] = tab.sum(axis=1)
tab1 = tab.transpose()
tab1["sum"] = tab1.sum(axis=1)
list = list(tab1)


#### calulating a percentage value
for i in range(len(list)-1):
    n = list[i]
    name = "weighted " + n
    tab1[name] = ""
    num = tab1.columns.get_loc(name)
    for j in range(len(tab1)):
        tab1.iloc [j, num] = round((tab1.iloc[j,i]/tab1.iloc[-1,i])*100,2)

print(tab1.columns.to_list)

tab2 = tab1 [['weighted A', 'weighted B','weighted C'] ]
tab2.columns= ['A','B','C']

df = tab2.drop(tab2.index[-1])
index_list = df.index.values.tolist()


######Draw a vertical bar chart
pos = []
for i in range(len(df['C'])):
    pos.append(i)
width = 0.25
print(pos)
print([p + width for p in pos])

# # Plotting the bars
plt.rcParams['font.family'] = "sans-serif"
fig, ax = plt.subplots(figsize=(10,7))


# Create a bar with first data,
# in position pos,
plt.bar(pos,
        #using df['pre_score'] data,
        df['A'],
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#3ca3bf',
        edgecolor='black',
        # with label the first value in first_name
        label= 'A',
 )


# Create a bar with second data,
# in position pos + some width buffer,
plt.bar([p + width for p in pos],
        #using df['mid_score'] data,
        df['B'],
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#f68b37',
        edgecolor='black',
        # with label the second value in first_name
        label='B')

# Create a bar with second data,
# in position pos + some width buffer,
plt.bar([p + 2*width for p in pos],
        #using df['mid_score'] data,
        df['C'],
        # of width
        width,
        # with alpha 0.5
        alpha=0.5,
        # with color
        color='#735698',
        edgecolor='black',
        # with label the second value in first_name
        label='C')


# Set the y axis label
ax.set_ylabel('Frequency',fontsize=11 , labelpad=10)
plt.yticks(fontsize=8)

# Set the y axis label
ax.set_xlabel('Attributes',fontsize=11 , labelpad=10)


# Set the position of the x ticks
ax.set_xticks([p + 1 * width for p in pos])

plt.xticks( rotation=40)
plt.xticks(fontsize=10, ha='right')

# Set the labels for the x ticks
ax.set_xticklabels(index_list)
plt.subplots_adjust(bottom=.34, top=0.98)


# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*4)
plt.ylim([0, max(df['C'] + df['B'])])


##### ajusting the legend
plt.legend( ['A','B', 'C'], loc='upper right', )
plt.legend( prop={"size":8}, borderpad = .5 , labelspacing= 1.5 )


##### saving the image
rpath2 = "sid_by_side_barplot.png"
if os.path.exists(rpath2):
    os.remove(rpath2)
plt.savefig(rpath2, dpi =220)
plt.show()


