from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pymysql  # type: ignore
import os
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import PromptTemplate


load_dotenv()

# Inicializar FastAPI
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Inicializar el cliente del modelo
from huggingface_hub import InferenceClient  # type: ignore
client = InferenceClient(api_key=HUGGINGFACEHUB_API_TOKEN)

# Valores válidos para los parámetros
VALID_TIPOS = ["libro", "película", "videojuego", "juego de mesa", "podcast"]
VALID_EDADES = ["infantil", "juvenil", "adulto"]
VALID_GENEROS = ["ciencia ficción", "comedia", "drama", "romance", "fantasía", "acción", "terror", "guerra", "lucha"]

# Modelo para la solicitud de recomendaciones
class RecommendationRequest(BaseModel):
     tipo: str
     edad: str
     genero: str
     idioma: str = "español"
     cantidad: int = 5

# Crear un template de prompt con LangChain
recommendation_template = PromptTemplate(
     input_variables=["cantidad", "tipo", "edad", "genero", "idioma"],
     template=(
          "Eres un experto en recomendaciones culturales. Genera una lista de {cantidad} {tipo}s "
          "para un público {edad}, en el género {genero}, y en el idioma {idioma}. "
          "Proporciona las recomendaciones en el siguiente formato:\n\n"
          "Título: [Título de la recomendación]\n"
          "Descripción: [Breve descripción sobre la recomendación].\n\n"
          "Ejemplo:\n"
          "Título: La guerra de las galaxias\n"
          "Descripción: Una aventura épica de ciencia ficción dirigida por George Lucas.\n\n"
          "Lista de recomendaciones:"
     ),
)

# Función para conectar a la base de datos MySQL
def connect_to_db():
     return pymysql.connect(
          host=DB_HOST,
          user=DB_USER,
          password=DB_PASSWORD,
          database=DB_NAME,
          cursorclass=pymysql.cursors.DictCursor
     )


# Endpoint para servir el archivo index.html
@app.get("/web")
async def redirect_to_home():
     return RedirectResponse(url="/")

# Endpoint para servir el archivo index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
     try:
          # Verifica si el archivo index.html existe en el mismo directorio
          if not os.path.exists("index.html"):
               raise HTTPException(status_code=500, detail="El archivo index.html no se encuentra en el directorio.")

          # Leer el archivo index.html
          with open("index.html", "r", encoding="utf-8") as file:
               content = file.read()

          return HTMLResponse(content=content)

     except FileNotFoundError:
          raise HTTPException(status_code=500, detail="El archivo index.html no se encuentra en el directorio.")
     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error al leer el archivo index.html: {e}")

# Endpoint para obtener recomendaciones
@app.post("/get_recommendations")
async def get_recommendations(request: RecommendationRequest):
     # Validaciones
     if request.tipo.lower() not in VALID_TIPOS:
          raise HTTPException(
               status_code=422,
               detail=f"El tipo '{request.tipo}' no es válido. Los valores permitidos son: {', '.join(VALID_TIPOS)}."
          )
     if request.edad.lower() not in VALID_EDADES:
          raise HTTPException(
               status_code=422,
               detail=f"La edad '{request.edad}' no es válida. Los valores permitidos son: {', '.join(VALID_EDADES)}."
          )
     if request.genero.lower() not in VALID_GENEROS:
          raise HTTPException(
               status_code=422,
               detail=f"El género '{request.genero}' no es válido. Los valores permitidos son: {', '.join(VALID_GENEROS)}."
          )

     if request.cantidad >= 6:
          raise HTTPException(
               status_code=422,
               detail=f"La cantidad máxima permitida es 6."
          )

     try:
          # Generar el prompt utilizando LangChain PromptTemplate
          prompt = recommendation_template.format(
               cantidad=request.cantidad,
               tipo=request.tipo,
               edad=request.edad,
               genero=request.genero,
               idioma=request.idioma,
          )

          # Llamada al modelo con el prompt generado
          messages = [{"role": "user", "content": prompt}]
          completion = client.chat.completions.create(
               model="microsoft/Phi-3.5-mini-instruct",
               messages=messages,
               max_tokens=1150
          )

          # Extraer las recomendaciones
          response = completion.choices[0].message.content.strip()

          if not response:
               raise HTTPException(status_code=500, detail="El modelo no ha generado recomendaciones.")

          # Guardar las recomendaciones en la base de datos
          connection = connect_to_db()
          try:
               with connection.cursor() as cursor:
                    cursor.execute(
                         "INSERT INTO recomendaciones (tipo, edad, genero, idioma, cantidad, detalles) "
                         "VALUES (%s, %s, %s, %s, %s, %s)",
                         (request.tipo, request.edad, request.genero, request.idioma, request.cantidad, response)
                    )
                    connection.commit()
          except Exception as db_error:
               connection.rollback()
               raise HTTPException(status_code=500, detail="Error al guardar en la base de datos.")
          finally:
               connection.close()

          return {"result": response}

     except Exception as e:
          raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {e}")

if __name__ == '__main__':
     uvicorn.run(app, host="localhost", port=8000)
