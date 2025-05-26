import cv2
# import pytesseract
from pytesseract import Output
import pandas as pd
from PIL import Image
import numpy as np
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import requests

url = "https://70fd-34-139-19-251.ngrok-free.app/image/"

def extracted_table(img_path):
    
    files = {'file': (img_path.name, img_path, img_path.type)}
    response = requests.post(url, files=files)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        print("Type of data:", type(data))
        print("Data:", data)
        if isinstance(data, dict) and 'data' in data:
            df_text = pd.DataFrame(data['data'])
        elif isinstance(data, list):
            df_text = pd.DataFrame(data)
        else:
            raise Exception("Unexpected response format from server.")

        print(df_text.head())
        return df_text
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
