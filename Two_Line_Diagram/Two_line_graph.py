##### Writer : "Atia"


###### Importign the Library
import os
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 20)
import matplotlib.pyplot as plt

os.chdir("/Users/macbook/Documents/pyhton/portfolio/Two_Line_Diagram")

#### reading the reference list
path = "renamed.xlsx"
dd = pd.read_excel(path)
d = dd[["city", "source", "tag", "new_tag"]]

#### Find all the unique values in new_tag_dimension
dimensions = d.new_tag.unique()


def lineplot (dim):
    d["binary"] = np.where(d["new_tag"] == dim, d["tag"], "other_tags")
    df = d[["source", "binary"]]
    tab = pd.pivot_table(df, index="source", columns="binary", aggfunc=len)
    tab = tab.fillna(0)

    tab["sum"] = tab.sum(axis=1)

    #####make a copy for normalizaiton
    tab_Nor = tab.copy()
    tab = tab.drop(['other_tags', "sum"], axis=1)
    tab["sum"] = round(tab.sum(axis=1), 2)
    tab = tab.fillna(0)

    list = tab_Nor.columns.to_list()
    for i in range(len(tab_Nor)):
        for j in range(len(list) - 1):
            tab_Nor.iloc[i, j] = round(((tab_Nor.iloc[i, j] / tab_Nor.iloc[i, -1]) * 100), 2)

    tab_Nor = tab_Nor.drop(["sum", 'other_tags'], axis=1)
    tab_Nor["sum"] = round(tab_Nor.sum(axis=1), 2)
    tab_Nor = tab_Nor.fillna(0)
    tab_Nor = tab_Nor.drop(["sum"], axis=1)
    tab_Nor= tab_Nor.transpose()


    #############################################
    ###### with respect to internal percentages

    da = d[d["new_tag"] == dim]
    da = da[["source", "tag"]]
    tab2 = pd.pivot_table(da, index="source", columns="tag", aggfunc=len)
    tab2 = tab2.fillna(0)

    tab2["sum"] = tab2.sum(axis=1)
    list2 = tab2.columns.to_list()

    for i in range(len(tab2)):
        for j in range(len(list2) - 1):
            tab2.iloc[i, j] = (round(((tab2.iloc[i, j] / tab2.iloc[i, -1]) * 100), 2))

    tab2 = tab2.drop(["sum"], axis=1)
    tab2_n= tab2.transpose()




    index_list = tab_Nor.index.values.tolist()

    # # Plotting the bars
    plt.rcParams['font.family'] = "sans-serif"

    fig, axs = plt.subplots(2, figsize=(12,16))



    # Create a bar with first data,



    axs[0].plot(tab_Nor ['Official Websites'],

        # with alpha 0.5
        alpha=0.8,
        # with color
        color='#3ca3bf',

        # with label the first value in first_name
        label= 'Official Websites',
        linewidth=2.0)


    axs[0].plot(tab_Nor['Personal Blogs'],

                 # with alpha 0.5
                 alpha=0.8,
                 # with color
                 color='#f68b37',

                 # with label the first value in first_name
                 label='Personal Blogs',
                 linewidth=2.0
                 )

        # Create a bar with second data,
    axs[0].plot(tab_Nor['Third Party Websites'],

                 # with alpha 0.5
                 alpha=0.8,
                 # with color
                 color='#735698',

                 # with label the first value in first_name
                 label='Third Party Websites',
                 linewidth=2.0
                 )


    axs[0].set_xticklabels(index_list, rotation=45, fontsize=10, ha='right')

    axs[0].set_ylabel('Image Frequency', fontsize=10, labelpad=10)
    axs[0].set_title('The Frequency of %s Attributes Compared to All Data ' %dim, fontsize=12, pad=20,
                  fontname='Times New Roman')
    axs[0].set_xlabel('Image Attributes', fontsize=10, labelpad=10)
    axs[0].xaxis.grid()


    ##### Ajusting the legend
    axs[0].legend(['Official Websites', 'Personal Blogs', 'Third Party Websites'])
    axs[0].legend(prop={"size": 4}, borderpad=.5, labelspacing=1.5)

    axs[0].legend(loc='upper left', bbox_to_anchor=(0.01, .99), ncol=3,
               borderaxespad=.2, prop={"size": 4})


    ########################
    ########################
    # Create the second image
    axs[1].plot(tab2_n['Official Websites'],

        alpha=0.8,
        # with color
        color='#3ca3bf',

        # with label the first value in first_name
        label= 'Official Websites',
        linewidth=2.0
        )

    axs[1].plot(tab2_n['Personal Blogs'],

                 # with alpha 0.5
                 alpha=0.8,
                 # with color
                 color='#f68b37',

                 # with label the first value in first_name
                 label='Personal Blogs',
                 linewidth=2.0
                 )

    # Create a bar with second data,
    axs[1].plot(tab2_n['Third Party Websites'],

                 # with alpha 0.5
                 alpha=0.8,
                 # with color
                 color='#735698',

                 # with label the first value in first_name
                 label='Third Party Websites',
                 linewidth=2.0
                 )

    axs[1].set_xticklabels(index_list, rotation=45, fontsize=9, ha='right')

    axs[1].set_ylabel('Image Frequency', fontsize=12, labelpad=10)
    axs[1].set_title('The Frequency of  %s Attributes Compared to Each other' %dim, fontsize=11, pad=20,
                  fontname='Times New Roman')
    axs[1].set_xlabel('Image Attributes', fontsize=12, labelpad=10)
    axs[1].xaxis.grid()


    ##### Ajusting the legend
    axs[1].legend(['Official Websites', 'Personal Blogs', 'Third Party Websites'])
    axs[1].legend(prop={"size": 10}, borderpad=.5, labelspacing=1.5)

    axs[1].legend(loc='upper left', bbox_to_anchor=(0.01, .99), ncol=3,
               borderaxespad=.2, prop={"size": 10})
    ######## arrancing the xticks
    plt.subplots_adjust( wspace=0.3, hspace=.6,bottom=.15 )


    ##### saving the files
    file = ('%s Line plot.png' % dim)
    path = "pictures"
    figname = os.path.join(path, file)

    if os.path.exists(figname):
        os.remove(figname)

    plt.savefig(figname, dpi= 180)
    # plt.show()



for i in dimensions:
    lineplot(i)