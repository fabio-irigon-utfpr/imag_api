##Para teste local:
### Navegar para a pasta local
python -m venv myenv
myenv\Scripts\activate  (se linux: source myenv/bin/activate)

###Instalação
pip install --upgrade pip
pip install -r requirements.txt 

###Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8081

###URL externa
https://imag-api.onrender.com/

###Comando para teste
curl -X POST -F "file=@im4.jpeg" https://imag-api.onrender.com/process
