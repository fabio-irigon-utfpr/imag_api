from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np

#uvicorn main:app --reload

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "API FastAPI + OpenCV ativa!!"}

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    """
    Endpoint de processamento — recebe imagem e retorna média de brilho.
    """
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = float(np.mean(gray))
    return {"mean_brightness": mean_brightness}



@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    """
    Página simples para upload de imagem.
    """
    return templates.TemplateResponse("upload.html", {"request": request})

