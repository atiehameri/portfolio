###### Writer : "Atia"

####Importing Libraries
from urllib.request import Request, urlopen
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import shutil


os.chdir("/Users/macbook/Documents/pyhton/portfolio/Collecting_Image")


city= "sacramento"
url = "https://www.visitsacramento.com/"
sec = "https://www.visitsacramento"

folder_name = "city"

#### removing the folder if it already exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)


##### setting up saving teh images
image_name = ("%s/%s_image" %(city,city))
if not os.path.exists(image_name ):
    os.makedirs(image_name )



##### opening and saving the links
req = Request(url)
html_page = urlopen(req)
soup = BeautifulSoup(html_page)

links = [url]
for link in soup.findAll('a'):
    links.append(link.get('href'))


all_data= []
for i in links:
    try:
        if sec in i:
            all_data.append(i)
    except:
        print("no")

data= [url]


for i in all_data:
    if not i in data:
        data.append(i)
        print(i)

second = []

for i in data:
    req = Request(i)
    try:
        html_page = urlopen(req)
    except:
        pass
    soup = BeautifulSoup(html_page)

    temp = []
    for link in soup.findAll('a'):
        temp.append(link.get('href'))




    for i in temp:
        try:
            if sec in i:
                print(i)

                second.append(i)
        except:
            print("print(no")




for i in second:
    if not i in data:
        data.append(i)
        print(i)


print(len(data))



table = []
count = 0

for site in data:
    r = requests.get(site)
    # Parse HTML Code
    soup = BeautifulSoup(r.text, 'html.parser')
    # find all images in URL
    images = soup.findAll('img')


    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            print(count)
            print("printing link:    ", i, image)
            # From image tag ,Fetch image Source URL
            # 1.data-srcset
            # 2.data-src
            # 3.data-fallback-src
            # 4.src
            # se exception handling
            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-lazy-src"]

                # then we will search for "data-src" in img
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["data-srcset"]

                            # if no Source URL found
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # After checking above condition, Image Download start
                    name = ("images%s.jpg"%count)

                    fname = os.path.join(image_name, name)


                    if os.path.exists(fname):
                        os.remove(fname)


                    with open(fname, "wb+") as f:
                        f.write(r)

                        # counting number of image downloaded
                    count += 1
                    number=  ("images%s.jpg"%count)
                    temp = [city, site,number, count ]
                    table.append(temp)
                    print(temp)
            except:
                pass

        # There might be possible, that all
        # images not download
        # if all images download
        if count == len(images):
            print("All Images Downloaded!")

            # if all images not download
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")



df = pd.DataFrame(table)
name = ("%s_excel_image.xlsx" %city)

df.to_excel(name)


##### removing he tumbnails
filter_folder = ("%s/%s_image_filter"%(city,city))
if not os.path.exists(filter_folder):
    os.makedirs(filter_folder)
count = 0
for root, dir, files in os.walk(image_name) :

    for file  in files:
        dis = os.path.join(image_name, file)
        img = Image.open(dis)
        if img.size[0] > 30:
            shutil.copy(dis, filter_folder)
            count +=1

# fname = "sacramento.xlsx"

##### saving the final files
df = pd.read_excel(name)
df.columns = ["number", "city", "link", "name", "number"]
print(len(df))
names= []
for root, dir, files in os.walk(filter_folder):
    for file in files:

        print(type(file))
        t = file.split(".")
        print(t)
        name = t[0][:5]+"_"+t[0][6:]
        print(name)
        names.append(name)
        print(name)
dn = pd.DataFrame(names)
dn.columns = ["name"]

print(len(dn))
data = pd.merge(df, dn, on= "name", how= "outer")
print(len(data))

data = data[["city", "link", "name"]]
name = ("%s_final_ready.xlsx"%city)
nn = os.path.join(folder_name,name )
data.to_excel(nn)


