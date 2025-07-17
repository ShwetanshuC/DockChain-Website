'''
For this to work properly, you need to set up a conda environment, and in the conda prompt, 
you need to use pip to install all the libraries you're going to use. 
Using the default vscode prompt won't do anything, and will show as if the modules are not recognized. 
In some cases, you need to tweak the base path of the terminal so that python can be found.

- install conda
- open conda terminal
- cd to website folder
- accept terms of service
- create virtual environment using "conda create --name [DESIRED NAME OF ENVIRONMENT] python=3.11"
- "conda install pip"
- install dependencies ("pip install [PACKAGE]"):
    mysql
    mysql-connector-python
    django
    easyocr
    openai
- activate venv: "conda activate [DESIRED NAME OF ENVIRONMENT]"
- run webserver: python manage.py runserver
'''


import os
from typing import List
import easyocr
import warnings
import openai 
from openai import OpenAI
import mysql.connector

warnings.filterwarnings("ignore")

#setting up the ocr reader 
reader= easyocr.Reader(['en'], gpu=True)
#-----------------------------------------------------

#Takes the IMAGE path and returns recognized text
def ocr_scan(imagePath: str) -> str:
    result = reader.readtext(str(imagePath))
    recognizedText = " ".join(elem[1] for elem in result)
    return recognizedText

#image_path ='C:\Users\ashok\Downloads\licenseimages\texasPlate.jpg'
#image_path = "./dirtyTexasPlate.jpg"

valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
#------------------------------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="S/g041408",
    database="truckers"
)
cursor = conn.cursor()


#-------------------------------------------------------

#takes the FOLDER path and returns recognized text in EVERY image in the folder
def folder_scan(folderPath: str) -> str:
    listOfPlateNumbers = []
    print("Going through the path....", folderPath)
    
    #This for loop goes through all the items in the folder and runs the above function ^^^ for EVERY one
    for file in os.listdir(folderPath):
        #print(file + ": ")
        file_path = os.path.join(folderPath, file)
        
        raw_file_path = file_path.replace("\\", "/")
        print(extract_new_license_plate(ocr_scan(raw_file_path)))
        listOfPlateNumbers.append(extract_new_license_plate(ocr_scan(raw_file_path)))

        '''
        
        ext = os.path.splitext(file)[1].lower()

        if ext in valid_extensions:
            ocr_scan(file_path)
            '''

    return listOfPlateNumbers

#print("Here is the extracted text:", ocr_scan(image_path))



#print(folder_scan(folder_path))
#-----------------------------------------------

#The OpenAI stuff starts here:

client = OpenAI(api_key="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")

'''
def extract_license_plate(ocr_text: str) -> str:
    prompt = f"""
You are an expert assistant who extracts ONLY license plate numbers from the text below. License plates may include letters and numbers, and are 6 digits long.
All 6 digits may be together, or they may have a space in between, with three characters, a space, and three more characters. 
Alternatively, there may be a dot in between the sets of three characters. Alternatively, there may be other redundant letters in between the two sets of three letters. 
Your job is to take the inputted text below, extract the license plate numbers, and return the 6 characters without any spaces. 
The text may include state names or extra words.
Extract only the license plate number.

Text: "{ocr_text}"
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response['choices'][0]['message']['content'].strip()

'''

def extract_new_license_plate(ocr_text: str) -> str:
    prompt = f"""
Extract ONLY the license plate number from the following OCR result. 
License plates may include letters and numbers, and are 6 digits long.
All 6 digits may be together, or they may have a space in between, with three characters, a space, and three more characters. 
Alternatively, there may be a dot in between the sets of three characters. Alternatively, there may be other redundant letters in between the two sets of three letters. 
Your job is to take the inputted text below, extract the license plate numbers, and return the 6 characters without any spaces. 
The text may include state names or extra words.
Ignore any state names, slogans, or irrelevant text.

OCR text: "{ocr_text}"

Only return the license plate number.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[ERROR] {e}"







'''
def is_plate_registered(plate_number: str):
    print("Hey i'm here")
    cursor.execute("SELECT id FROM truckmanagement_licenseplate WHERE plate_number = %s", (plate_number,))
    result = cursor.fetchone()

    print(result)


    if not result:
        print("oops it didn't work")
        return False

    vehicle_id = result[0]

    print("The vehicle id is", vehicle_id)

    # Step 2: Check if that vehicle ID is in registered_plates
    print(cursor.execute("SELECT license_plate_id FROM truckmanagement_job WHERE license_plate_id = %s", (vehicle_id,)))


    if cursor.fetchone() is not None:
        return "This plate exists"
        #print("this plate exists")

is_plate_registered("7ADBF3")


'''

#folder_path = r"C:\Users\ashok\Downloads\licenseimages"

#folder_scan(folder_path)





