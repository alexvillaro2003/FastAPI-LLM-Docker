# Recomendaciones Culturales 🎧📚

## Descripción
Aplicación web para obtener recomendaciones culturales personalizadas (📖 libro, 🎬 película, 🎮 videojuego, etc.), basada en tus preferencias. Usa **FastAPI** para el backend, **Hugging Face** para el procesamiento de datos y **MySQL** en AWS como base de datos.

## Tecnologías 🔧
- **FastAPI**: Framework para APIs.
- **Pydantic**: Validación de datos.
- **PyMySQL**: Conexión a MySQL en AWS.
- **Hugging Face**: Modelos de IA.
- **TailwindCSS**: Diseño moderno.
- **MySQL**: Base de datos en AWS.

## Requisitos ⚙️

- **Python 3.7+**  
- **MySQL** o base de datos compatible en **AWS**.

### Librerías Python

```bash
pip install -r requirements.txt
```

## Variables de entorno 🌿
Crea un archivo .env con las siguientes variables:

  - **DB_HOST**=tu_host_aws_rds
  - **DB_USER**=tu_usuario_mysql
  - **DB_PASSWORD**=tu_contraseña_mysql
  - **DB_NAME**=tu_base_de_datos
  - **HUGGINGFACEHUB_API_TOKEN**=tu_token_huggingface

## Ejecución 🚀

```bash
uvicorn main:app --reload
```

La app estará disponible en: http://localhost:8000.

## Uso 📝

1. Abre la página en tu navegador.
2. Rellena el formulario con tus preferencias.
3. Haz clic en **"Obtener Recomendaciones"** 🎉 y disfruta de las sugerencias.

## Endpoints 🖥️

- **GET `/web`**: Redirige a la página principal.
- **GET `/`**: Sirve el formulario.
- **POST `/get_recommendations`**: Recibe tus preferencias y devuelve recomendaciones.

## Parámetros del formulario 📋

- **Tipo de contenido**: 📖 Libro, 🎬 Película, 🎮 Videojuego, 🎲 Juego de Mesa, 🎙️ Podcast.
- **Edad recomendada**: 👶 Infantil, 🧑‍🎤 Juvenil, 👩‍🦳 Adulto.
- **Género**: 🚀 Ciencia Ficción, 😂 Comedia, 🎭 Drama, 💖 Romance, 🧚‍♀️ Fantasía, 💥 Acción, 👻 Terror, ⚔️ Guerra, 🥊 Lucha.
- **Cantidad**: Número de recomendaciones (máximo 6).

## Librerías y Versiones 📚

El proyecto utiliza las siguientes librerías:

- **FastAPI**: `0.115.5`
- **Pydantic**: `2.9.2`
- **PyMySQL**: `1.1.1`
- **python-dotenv**: `1.0.1`
- **Uvicorn**: `0.32.1`
- **LangChain**: `0.3.9`
- **Huggingface Hub**: `0.26.3`

## Contribuciones 🤝

¡Si deseas contribuir, abre un _pull request_ o crea un _issue_!

---

🎉 ¡Gracias por usar Recomendaciones Culturales! 🎧📚
