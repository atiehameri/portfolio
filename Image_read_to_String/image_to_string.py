import pandas as pd
import re
import os
from PIL import Image, ImageEnhance, ImageFilter
import PIL.Image
import pytesseract

##### the purpose of this project is to open an passport image, turn it to a text string,
##### Then extract the name, last name,  passport number,  date of birth, and place of bith
#### and save in into a table
os.chdir("/Users/macbook/Documents/pyhton/portfolio/Image_read_to_String/image_to_string.py")

address = "PASSPIC2.jpg"

##### read teh image with PIL
im = Image.open(address)
im = im.convert('L')                             # grayscale
im = im.point(lambda x: 0 if x < 140 else 255)   # threshold (binarize)

##### Turn in into string
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/Cellar/tesseract/4.1.1/bin/tesseract"
line = pytesseract.image_to_string(im)


###### using regex to extract
#### find tha last name
regex_surname = (r'\sSurname[.:\s]*(.+)\s')
surname= re.findall(regex_surname,line)
print(surname)

#### find tha first name
regex_name = (r'\nName[.:\s]*(\w*)\.*\s')
name = re.findall(regex_name,line)
print(name)

####passport number
regex_pass_number = (r'\sPassport No (.+)\s')
pass_number = re.findall(regex_pass_number,line)
print(pass_number)

####date of birth
dateofbirth_number = (r'\sDate.*th[.:\s]*(\d{2}/\d{2}/\d{4})\s')
dateofbirth=  re.findall(dateofbirth_number,line)
print(dateofbirth)

####place of birth
placebirth_loc= (r'\sDate.*-\s(\w+)\s')
placebirth = re.findall(placebirth_loc,line)
print(placebirth)

list = {"Last Name": surname, "Name": name, "Passport Number": pass_number,
        'Date of Birth':dateofbirth, "Place of Birth": placebirth}
table = pd.DataFrame(list)

name = "/Users/macbook/Documents/PhD/Image_read_to_String/data.xlsx"
table.to_excel("data.xlsx")
