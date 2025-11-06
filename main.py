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


@app.post("/process_any")
async def process_image_flexible(request: Request):
    """
    Endpoint alternativo — aceita qualquer nome de campo (para testes)
    """
    form = await request.form()
    debug_info = {}

    # lista tudo que chegou no corpo
    for key, value in form.items():
        if hasattr(value, "filename"):
            debug_info[key] = {
                "filename": value.filename,
                "content_type": value.content_type,
                "is_uploadfile": True
            }
        else:
            debug_info[key] = {
                "value_preview": str(value)[:100],
                "is_uploadfile": False
            }

    if not any(hasattr(v, "filename") for v in form.values()):
        return {
            "error": "nenhum arquivo encontrado no upload",
            "detalhes_recebidos": debug_info
        }

    # procura o primeiro arquivo enviado no formulário
    file = next((v for v in form.values() if hasattr(v, "filename")), None)
    if not file:
        return {"error": "nenhum arquivo encontrado no upload"}

    # lê e processa o arquivo da mesma forma
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mean_brightness = float(np.mean(gray))

    return {
        "mean_brightness": mean_brightness,
        "filename": file.filename,
        "field_name": [k for k, v in form.items() if v is file][0],
    }


@app.get("/upload", response_class=HTMLResponse)
def upload_form(request: Request):
    """
    Página simples para upload de imagem.
    """
    return templates.TemplateResponse("upload.html", {"request": request})

