import requests
from datetime import datetime

class DatosClimaticos:
    def __init__(self, ciudad, coordenadas, pronostico, actividades, calidad_aire, indices):
        self.ciudad = ciudad
        self.coordenadas = coordenadas
        self.pronostico = pronostico
        self.actividades = actividades
        self.calidad_aire = calidad_aire
        self.indices = indices

    def to_dict(self):
        return {
            "ciudad": self.ciudad,
            "coordenadas": self.coordenadas,
            "pronostico": self.pronostico,
            "actividades": self.actividades,
            "calidad_aire": self.calidad_aire,
            "indices": self.indices
        }

class ServicioClima:
    def __init__(self):
        self.headers = {'User-Agent': 'ClimaApp/1.0'} 

    def _obtener_coordenadas(self, ciudad):
        """Busca latitud y longitud en OpenStreetMap"""
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {'q': ciudad, 'format': 'json', 'limit': 1}
            respuesta = requests.get(url, params=params, headers=self.headers)
            datos = respuesta.json()
            
            if datos:
                return {
                    "lat": float(datos[0]['lat']), 
                    "lon": float(datos[0]['lon']),
                    "nombre": datos[0]['display_name'].split(',')[0]
                }
        except Exception as e:
            print(f"Error Geocoding: {e}")
        
        return {"lat": 19.4326, "lon": -99.1332, "nombre": "No encontrada"}

    def _interpretar_wmo(self, code):
        """Traduce códigos WMO (0, 1, 2...) a iconos y descripciones"""
        if code == 0: return "sun", "Despejado"
        if code in [1, 2, 3]: return "cloud-sun", "Nublado"
        if code in [45, 48]: return "smog", "Niebla"
        if code in [51, 53, 55]: return "cloud-rain", "Llovizna"
        if code in [61, 63, 65]: return "cloud-showers-heavy", "Lluvia"
        if code in [80, 81, 82]: return "cloud-showers-heavy", "Chubascos"
        if code in [95, 96, 99]: return "bolt", "Tormenta"
        return "cloud", "Variable"

    def _obtener_datos_api(self, lat, lon):
        """Consulta Open-Meteo para Clima y Calidad del Aire"""
        try:
            url_clima = "https://api.open-meteo.com/v1/forecast"
            params_clima = {
                "latitude": lat,
                "longitude": lon,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max,uv_index_max",
                "current_weather": "true",
                "timezone": "auto"
            }
            res_clima = requests.get(url_clima, params=params_clima).json()
            url_aire = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params_aire = {
                "latitude": lat,
                "longitude": lon,
                "current": "us_aqi,pm2_5",
                "timezone": "auto"
            }
            res_aire = requests.get(url_aire, params=params_aire).json()

            return res_clima, res_aire
        except Exception as e:
            print(f"Error API: {e}")
            return None, None

    def obtener_datos_tablero(self, ciudad_busqueda="Guadalajara"):
        ubi = self._obtener_coordenadas(ciudad_busqueda)
        
        clima_data, aire_data = self._obtener_datos_api(ubi["lat"], ubi["lon"])

        if not clima_data or not aire_data:
            return self._datos_fallback(ubi)

        # Pronostico (Próximos 5 días)
        pronostico = []
        daily = clima_data.get("daily", {})
        dias = daily.get("time", [])
        
        for i in range(min(5, len(dias))):
            fecha_obj = datetime.strptime(dias[i], "%Y-%m-%d")
            nombre_dia = fecha_obj.strftime("%a %d") # Ej: Mon 05
            
            codigo_wmo = daily["weathercode"][i]
            icono, _ = self._interpretar_wmo(codigo_wmo)
            
            pronostico.append({
                "dia": nombre_dia,
                "max": round(daily["temperature_2m_max"][i]),
                "min": round(daily["temperature_2m_min"][i]),
                "icono": icono,
                "prob_lluvia": daily["precipitation_probability_max"][i]
            })

        aqi = aire_data["current"]["us_aqi"]
        pm25 = aire_data["current"]["pm2_5"]
        
        nivel_aire = "Buena"
        if aqi > 50: nivel_aire = "Moderada"
        if aqi > 100: nivel_aire = "Mala"
        if aqi > 150: nivel_aire = "Poc. Saludable"

        datos = DatosClimaticos(
            ciudad=ubi["nombre"],
            coordenadas={"lat": ubi["lat"], "lon": ubi["lon"]},
            pronostico=pronostico,
            actividades=[
                {
                    "titulo": "Correr", 
                    "estado": "Condiciones reales obtenidas.", 
                    "icono": "person-running", 
                    "color": "success" if daily["precipitation_probability_max"][0] < 30 else "warning"
                },
                {
                    "titulo": "Índice de Polen", 
                    "estado": "Riesgo bajo en esta estación.", 
                    "icono": "seedling", 
                    "color": "success"
                }
            ],
            calidad_aire={
                "valor": aqi,
                "nivel": nivel_aire,
                "particulas": f"{pm25}"
            },
            indices=[
                {"nombre": "Índice UV (Max)", "valor": str(daily["uv_index_max"][0]), "icono": "sun", "color": "orange"},
                {"nombre": "Prob. Lluvia", "valor": f"{daily['precipitation_probability_max'][0]}%", "icono": "umbrella", "color": "blue"},
                {"nombre": "Viento", "valor": f"{clima_data['current_weather']['windspeed']} km/h", "icono": "wind", "color": "green"},
            ]
        )
        return datos.to_dict()

    def _datos_fallback(self, ubi):
        """Datos de respaldo por si falla internet"""
        return {
            "ciudad": ubi["nombre"],
            "coordenadas": {"lat": ubi["lat"], "lon": ubi["lon"]},
            "pronostico": [],
            "actividades": [],
            "calidad_aire": {"valor": 0, "nivel": "Error", "particulas": "--"},
            "indices": []
        } 