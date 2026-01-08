let map = null;

document.addEventListener("DOMContentLoaded", () => {
    cargarDatos("Guadalajara");
    document.getElementById("input-ciudad").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            buscarCiudad();
        }
    });
});

function buscarCiudad() {
    const input = document.getElementById("input-ciudad");
    const ciudad = input.value.trim();
    if (ciudad) {
        cargarDatos(ciudad);
    }
}

async function cargarDatos(ciudad) {
    try {
        const response = await fetch(`/api/clima?ciudad=${ciudad}`);
        if (!response.ok) throw new Error("Error en servidor");
        
        const data = await response.json();
        
        // Actualizamos el título de la ubicación
        document.getElementById("ciudad-titulo").innerText = `Reporte para: ${data.ciudad}`;
        // Renderizamos los datos
        renderizarPronostico(data.pronostico);
        renderizarActividades(data.actividades);
        renderizarAire(data.calidad_aire);
        renderizarIndices(data.indices);
        // Actualizamos el mapa a las nuevas coordenadas
        actualizarMapa(data.coordenadas.lat, data.coordenadas.lon);

    } catch (error) {
        console.error("Error:", error);
        alert("No se pudo encontrar la ciudad o hubo un error.");
    }
}

function actualizarMapa(lat, lon) {
    if (map === null) {
        map = L.map('map').setView([lat, lon], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap'
        }).addTo(map);
    } else {
        map.flyTo([lat, lon], 12);
    }

    // Se remueven marcadores anteriores
    map.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
            map.removeLayer(layer);
        }
    });

    // Agregamos un marcador en la nueva ciudad
    L.marker([lat, lon]).addTo(map)
        .bindPopup("Ubicación actual")
        .openPopup();
}

function renderizarPronostico(dias) {
    const container = document.getElementById('forecast-container');
    container.innerHTML = '';
    dias.forEach(d => {
        let iconClass = 'fa-sun text-warning';
        if(d.icono.includes('cloud')) iconClass = 'fa-cloud text-secondary';
        if(d.icono.includes('rain')) iconClass = 'fa-cloud-rain text-primary';

        const html = `
            <div class="d-flex flex-column align-items-center mx-1">
                <small class="text-muted mb-2">${d.dia}</small>
                <i class="fas ${iconClass} fa-2x mb-2"></i>
                <div class="fw-bold text-dark">${d.max}° <span class="text-muted fw-normal" style="font-size:0.8em">/ ${d.min}°</span></div>
                <small class="text-primary" style="font-size: 0.75rem;">${d.prob_lluvia}%</small>
            </div>
        `;
        container.innerHTML += html;
    });
}

function renderizarActividades(actividades) {
    const container = document.getElementById('activities-container');
    container.innerHTML = '';
    actividades.forEach(act => {
        let colorClass = act.color === 'success' ? 'text-success' : 'text-warning';
        const html = `
            <div class="d-flex align-items-start mb-4">
                <div class="me-3"><i class="fas fa-${act.icono} fa-2x ${colorClass}"></i></div>
                <div><h6 class="mb-1 fw-bold text-dark">${act.titulo}</h6><small class="text-muted">${act.estado}</small></div>
            </div>
        `;
        container.innerHTML += html;
    });
}

function renderizarAire(aire) {
    const valElement = document.getElementById('air-quality-val');
    const textElement = document.getElementById('air-quality-text');
    const pmElement = document.getElementById('air-quality-pm');

    if(valElement) valElement.innerText = aire.valor;
    if(textElement) textElement.innerText = aire.nivel;
    if(pmElement) pmElement.innerText = aire.particulas;

    const circle = document.querySelector('.gauge-circle');
    if(circle) {
        if(aire.valor > 100) circle.style.borderColor = '#ef4444';
        else if(aire.valor > 50) circle.style.borderColor = '#f59e0b';
        else circle.style.borderColor = '#22c55e';
    }
}

function renderizarIndices(indices) {
    const container = document.getElementById('indices-container');
    container.innerHTML = '';
    indices.forEach(ind => {
        const html = `
            <div class="d-flex justify-content-between align-items-center mb-3">
                <div class="d-flex align-items-center">
                    <i class="fas fa-${ind.icono} me-3 text-primary" style="width:20px; text-align:center;"></i>
                    <span>${ind.nombre}</span>
                </div>
                <span class="badge bg-secondary rounded-pill px-3">${ind.valor}</span>
            </div>
        `;
        container.innerHTML += html;
    });
}