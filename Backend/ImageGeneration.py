import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

def open_images(prompt):
    folder_path = r"Data"  
    prompt = prompt.replace(" ", "_")  

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open image {image_path}")
        
API_URL = 'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0'
headers = {"Authorization": f"Bearer {get_key('.env', 'huggingfaceAPIkey')}"}
async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"API Error {response.status_code}: {response.text}")
            return None
        return response.content
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return None

async def generate_image(prompt:str):
        tasks = []
        for _ in range(1):
            payload = {
                        "inputs" : f"{prompt} , quality:4K , sharpness = maximum , Ultra High Details , high resolution , seed = {randint(0, 100000)}",                       
            }
            task = asyncio.create_task(query(payload))
            tasks.append(task)
        image_bytes_list = await asyncio.gather(*tasks)
        for i, image_bytes in enumerate(image_bytes_list):
             if image_bytes:  # Skip failed responses
                os.makedirs("Data", exist_ok=True)  # Redundant safety
                with open(f"Data/{prompt.replace(' ', '_')}{i+1}.jpg", "wb") as f:
                    f.write(image_bytes)
def GenterateImages(prompt:str):
    asyncio.run(generate_image(prompt))
    open_images(prompt)

while True:
    try:
        try:
            with open(r"Frontend/Files/ImageGeneration.data", "r") as f:
                Data = f.read().strip()
        except FileNotFoundError:
            Data = ""
        
        if not Data:
            sleep(1)
            continue
        
        Prompt, Status = Data.split(",")
        if Status.strip() == "True":
            print(f"Generating Image... ")
            ImageStatus = GenterateImages(prompt=Prompt)
            
            with open(r"Frontend/Files/ImageGeneration.data" , "w") as f:        
                f.write("False , False")
                break
        else:
            sleep(1)
    
    except:
        pass
         