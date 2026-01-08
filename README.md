# 🌦️ Dashboard Climático Full Stack

![Estado del Proyecto](https://img.shields.io/badge/Estado-Terminado-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)

Aplicación web interactiva que proporciona datos meteorológicos y de calidad del aire en tiempo real para cualquier ciudad del mundo.

![Captura de Pantalla del Dashboard](dashboard.png)

## ✨ Características Principales

* **Búsqueda Global:** Localiza cualquier ciudad mediante la API de OpenStreetMap y obtiene sus coordenadas automáticamente.
* **Clima en Tiempo Real:** Muestra temperatura, probabilidad de lluvia y pronóstico a 5 días usando la API de Open-Meteo.
* **Calidad del Aire (AQI):** Monitoreo preciso de partículas **PM2.5** con semáforo de colores (Bueno, Moderado, Dañino).
* **Mapa Interactivo:** Integración con **Leaflet.js** para visualizar la ubicación geográfica consultada dinámicamente.
* **Modal Educativo:** Ventana emergente interactiva que explica qué son las partículas PM2.5 y sus riesgos para la salud.

## 🛠️ Tecnologías Utilizadas

### Backend

* **Python 3**
* **Flask**

### Frontend

* **HTML5 / CSS3**
* **JavaScript (ES6)**
* **Bootstrap 5**
* **Leaflet.js**
* **FontAwesome**

### APIs y Datos

* **Open-Meteo API**: Datos del clima y calidad del aire (Sin API Key).
* **OpenStreetMap (Nominatim)**

## 🚀 Instalación y Uso

Sigue estos pasos para correr el proyecto en tu computadora:

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
    cd TU_REPOSITORIO
    ```

2. **Crear y activar un entorno virtual:**

    * Windows:

        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

    * Mac/Linux:

        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Instalar dependencias:**

    ```bash
    pip install flask requests
    ```

4. **Ejecutar la aplicación:**

    ```bash
    python app.py
    ```

5. **Abrir en el navegador:**

    La aplicación se abrirá automáticamente o puedes visitar: `http://127.0.0.1:5000`

## 📂 Estructura del Proyecto

```text
📂 weather-app
 ┣ 📂 static
 ┃ ┣ 📜 style.css       
 ┃ ┗ 📜 script.js       
 ┣ 📂 templates
 ┃ ┗ 📜 index.html     
 ┣ 📜 app.py            
 ┣ 📜 weather_service.py 
 ┗ 📜 README.md
