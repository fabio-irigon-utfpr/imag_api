from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API ativa com FastAPI + OpenCV!"}

@app.post("/process")
async def process(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean = float(np.mean(gray))
    return {"mean_brightness": mean}
