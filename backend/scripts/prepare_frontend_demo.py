"""Carga datos ficticios completos por la API sin imprimir contraseñas ni JWT."""
import argparse
import json
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://127.0.0.1:8000')
parser.add_argument('--credentials', type=Path, default=ROOT / '.local/demo_credentials.json')
args = parser.parse_args()
credentials = json.loads(args.credentials.read_text())
names = {
    'Objetivo': 'Mejorar la experiencia del cliente',
    'Proyecto': 'Transformación de atención digital',
    'Capacidad': 'Gestión de clientes',
    'Proceso': 'Atender solicitudes de servicio',
    'Aplicación': 'Portal de servicios',
}
with httpx.Client(base_url=args.base_url, timeout=20) as client:
    def request(method, path, **kwargs):
        response = client.request(method, '/api/' + path, **kwargs)
        response.raise_for_status()
        return response.json()

    auth = request('POST', 'auth/login', json={'correo': credentials['admin'], 'contrasena': credentials['password']})
    client.headers['Authorization'] = 'Bearer ' + auth['accessToken']
    try:
        sample = request('PUT', 'v1/demostraciones/arquitectura-ficticia-v1',
                         json={'muestraId': 'arquitectura-ficticia-v1', 'ficticia': True})
        for ident in sample['elementoIds']:
            element = request('GET', 'v1/elementos/' + ident, params={'incluirBaja': 'true'})
            kind_name = element['tipoElemento']['nombre']
            if kind_name in names and element['nombre'] == kind_name + ' ficticio':
                base = next(field for field in element['campos'] if field['esBaseNombre'])
                request('PATCH', 'v1/elementos/' + ident,
                        json={'valores': [{'campoId': base['id'], 'texto': names[kind_name]}]})

        layers = request('GET', 'v1/capas')['items']
        business = next(layer for layer in layers if layer['nombre'] == 'Negocio')
        kinds = request('GET', 'v1/tipos-elemento', params={'capaId': business['id']})['items']
        kind = next((kind for kind in kinds if kind['nombre'] == 'Proyecto de mejora'), None)
        if kind is None:
            kind = request('POST', 'v1/tipos-elemento', json={'nombre': 'Proyecto de mejora', 'capaId': business['id']})
        fields = {field['nombre']: field for field in kind['campos']}
        definitions = [
            {'nombre': 'Descripción', 'tipoDato': 'texto', 'obligatorio': True, 'opciones': []},
            {'nombre': 'Presupuesto', 'tipoDato': 'numero', 'obligatorio': False, 'opciones': []},
            {'nombre': 'Fecha objetivo', 'tipoDato': 'fecha', 'obligatorio': False, 'opciones': []},
            {'nombre': 'Etapa', 'tipoDato': 'seleccion', 'obligatorio': True,
             'opciones': [{'etiqueta': 'Planeado', 'orden': 0}, {'etiqueta': 'En curso', 'orden': 1}]},
        ]
        for definition in definitions:
            if definition['nombre'] not in fields:
                field = request('POST', 'v1/tipos-elemento/' + kind['id'] + '/campos', json=definition)
                fields[field['nombre']] = field
        base = next(field for field in fields.values() if field['esBaseNombre'])
        name = 'Digitalizar el seguimiento de solicitudes'
        existing = request('GET', 'v1/elementos', params={
            'tipoElementoId': kind['id'], 'q': name, 'incluirBaja': 'true'})['items']
        if not any(element['nombre'] == name for element in existing):
            request('POST', 'v1/elementos', json={'tipoElementoId': kind['id'], 'valores': [
                {'campoId': base['id'], 'texto': name},
                {'campoId': fields['Descripción']['id'], 'texto': 'Centralizar las solicitudes de clientes y permitir consultar su avance desde el portal de servicios.'},
                {'campoId': fields['Presupuesto']['id'], 'numero': 45000},
                {'campoId': fields['Fecha objetivo']['id'], 'fecha': '2026-12-15'},
                {'campoId': fields['Etapa']['id'], 'opcionId': fields['Etapa']['opciones'][0]['id']},
            ]})
    finally:
        request('DELETE', 'v1/sesiones/actual')
print('Demo ficticia lista: cinco categorías, una relación validada y un proyecto con los cuatro tipos de campo. La carga repetida no duplica registros.')
