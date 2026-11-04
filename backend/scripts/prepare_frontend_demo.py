"""Prepara el inventario ficticio por la API; no imprime credenciales ni JWT."""
import json
from pathlib import Path
import httpx

ROOT = Path(__file__).resolve().parents[2]
credentials = json.loads((ROOT / '.local/demo_credentials.json').read_text())
names = {
    'Objetivo': 'Mejorar la experiencia del cliente',
    'Proyecto': 'Transformación de atención digital',
    'Capacidad': 'Gestión de clientes',
    'Proceso': 'Atender solicitudes de servicio',
    'Aplicación': 'Portal de servicios',
}
with httpx.Client(base_url='http://127.0.0.1:8000', timeout=20) as client:
    response = client.post('/api/auth/login', json={'correo': credentials['admin'], 'contrasena': credentials['password']})
    response.raise_for_status()
    client.headers['Authorization'] = 'Bearer ' + response.json()['accessToken']
    response = client.put('/api/v1/demostraciones/arquitectura-ficticia-v1', json={'muestraId': 'arquitectura-ficticia-v1', 'ficticia': True})
    response.raise_for_status()
    for id_ in response.json()['elementoIds']:
        detail = client.get('/api/v1/elementos/' + id_)
        detail.raise_for_status()
        element = detail.json()
        kind = element['tipoElemento']['nombre']
        if kind in names and element['nombre'] == kind + ' ficticio':
            base = next(field for field in element['campos'] if field['esBaseNombre'])
            updated = client.patch('/api/v1/elementos/' + id_, json={'valores': [{'campoId': base['id'], 'texto': names[kind]}]})
            updated.raise_for_status()
    client.delete('/api/v1/sesiones/actual').raise_for_status()
print('Inventario ficticio listo para la demostración del frontend.')
