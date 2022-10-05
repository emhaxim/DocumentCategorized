#importing packages
import pdfplumber
import  pandas as pd
from googletrans import Translator
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import requests



#Fast Api
app = FastAPI()


class Information(BaseModel):
    URL: str
    
   

##@app.get("/")
##def read_root():
##   # return {"Hello": "World"}
##   return information

@app.post("/Information/")
async def create_information(information: Information):
    response = catagorize(information.URL)
    return response




excel_data = pd.read_excel('Documents title data set_V01.xlsx', sheet_name=None)



def func(text):
    #initialize the Translator
    translator = Translator()
    source_lan = "lt"  #ln is the code for linth Language
    translated_to= "en" #ei is the code for English Language
    translated_text = translator.translate(text, src=source_lan, dest = translated_to)
    return translated_text.text


def catagorize(url):
    URL = url
    #URL = 'https://jbg.lt/dokumentubankas/download/749'
    response = requests.get(URL)

    open('abc.pdf', 'wb').write(response.content)
    print(response)

    with pdfplumber.open('abc.pdf') as pdf: 
       text = pdf.pages[0]
       clean_text = text.filter(lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
       #print(clean_text.extract_text())
       data = func(clean_text.extract_text()).upper()
       print(data)
    #print(data.split())



    score = []



    for i in list(excel_data['Keywords']['Keywords']):
       try:
           #print(i)
           #temp = i.replace(' ','',1)
           temp = i.replace(' ','')
           temp = func(temp)
           temp = temp.replace(' ','')
           #print(temp)
          
           temp = temp.upper()
           temp = temp.split(',')
           temp = set(temp)
           temp = list(temp)
           count = 0
           #print(temp)
           
           for j in temp:
                if(j in data):
                    count += data.count(j)
                 #  print(j)
                 #  count += 1
           score.append(count)
       except:
           score.append(0)

    print(score)

    #Return the max value of the list
    max_value = max(score)

    #Find the index of the max value
    max_index = score.index(max_value)
    catg = excel_data['Keywords']['Categorie'][max_index]


    print(f' \n \n Document belongs to {catg}')


    information = {"Catagorie":catg,
                   "Document":data[:50]}

    return information

    

















