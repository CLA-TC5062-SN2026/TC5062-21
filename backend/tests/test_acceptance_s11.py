"""Criterios de aceptación que no tenían un escenario explícito en S09."""
from uuid import uuid4

import pytest


@pytest.mark.parametrize('change', [{'rol': 'Consulta'}, {'activo': False}])
def test_last_administrator_cannot_be_removed(api, admin_token, change):
    headers = {'Authorization': 'Bearer ' + admin_token}
    profile = api.get('/api/auth/me', headers=headers).json()
    response = api.patch('/api/v1/usuarios/' + profile['id'], headers=headers, json=change)
    assert response.status_code == 409
    assert response.json()['codigo'] == 'ULTIMO_ADMINISTRADOR'
    current = api.get('/api/auth/me', headers=headers)
    assert current.status_code == 200
    assert current.json()['rol'] == 'Administrador' and current.json()['activo']


@pytest.fixture
def relation_scenario(api, admin_token):
    headers = {'Authorization': 'Bearer ' + admin_token}

    def post(path, body):
        response = api.post('/api/v1/' + path, headers=headers, json=body)
        assert response.status_code == 201, response.text
        return response.json()

    layer = post('capas', {'nombre': 'Aceptación S11-' + uuid4().hex})
    source_type = post('tipos-elemento', {'nombre': 'Proyecto', 'capaId': layer['id']})
    target_type = post('tipos-elemento', {'nombre': 'Capacidad', 'capaId': layer['id']})

    def element(kind, name):
        return post('elementos', {'tipoElementoId': kind['id'], 'valores': [
            {'campoId': kind['campos'][0]['id'], 'texto': name}]})

    origin = element(source_type, 'Mejora de atención digital')
    alternative = element(source_type, 'Renovación del portal')
    destination = element(target_type, 'Atención al cliente')
    kind = post('tipos-relacion', {'nombre': 'Mejora S11-' + uuid4().hex, 'descripcion': 'Mejora una capacidad',
                                 'tipoOrigenId': source_type['id'], 'tipoDestinoId': target_type['id']})
    payload = {'operacion': 'alta', 'origenId': origin['id'], 'destinoId': destination['id'],
               'tipoRelacionId': kind['id'], 'justificacion': 'El proyecto mejora la atención al cliente.'}
    return headers, post, origin, alternative, payload


def test_relation_rejection_change_and_retirement_require_decision(api, relation_scenario):
    headers, post, origin, _, payload = relation_scenario
    rejected = post('propuestas-relacion', payload)
    result = post('propuestas-relacion/' + rejected['id'] + '/decisiones', {'decision': 'rechazar'})
    assert result['propuesta']['estado'] == 'rechazada' and 'relacion' not in result
    map_route = '/api/v1/mapas/' + origin['id']
    assert api.get(map_route, headers=headers).json()['aristas'] == []

    accepted = post('propuestas-relacion', payload)
    relation = post('propuestas-relacion/' + accepted['id'] + '/decisiones', {'decision': 'aprobar'})['relacion']
    route = '/api/v1/relaciones/' + relation['id']
    change_payload = {**payload, 'operacion': 'cambio', 'relacionId': relation['id'],
                      'versionBase': relation['version'], 'justificacion': 'Mejora validada para el canal digital.'}
    change = post('propuestas-relacion', change_payload)
    assert api.get(route, headers=headers).json()['justificacion'] == payload['justificacion']
    changed = post('propuestas-relacion/' + change['id'] + '/decisiones', {'decision': 'aprobar'})['relacion']
    assert changed['id'] == relation['id'] and changed['justificacion'] == change_payload['justificacion']
    retirement = post('propuestas-relacion', {'operacion': 'retiro', 'relacionId': relation['id'],
                      'versionBase': changed['version'], 'justificacion': 'La iniciativa concluyó y se retira el vínculo.'})
    assert api.get(route, headers=headers).json()['estado'] == 'vigente'
    post('propuestas-relacion/' + retirement['id'] + '/decisiones', {'decision': 'aprobar'})
    assert api.get(route, headers=headers).json()['estado'] == 'retirada'
    assert api.get(map_route, headers=headers).json()['aristas'] == []


def test_inactive_new_origin_keeps_change_pending_and_current_relation(api, relation_scenario):
    headers, post, _, alternative, payload = relation_scenario
    proposal = post('propuestas-relacion', payload)
    relation = post('propuestas-relacion/' + proposal['id'] + '/decisiones', {'decision': 'aprobar'})['relacion']
    change = post('propuestas-relacion', {**payload, 'operacion': 'cambio', 'relacionId': relation['id'],
                  'versionBase': relation['version'], 'origenId': alternative['id']})
    assert api.delete('/api/v1/elementos/' + alternative['id'], headers=headers).status_code == 200
    response = api.post('/api/v1/propuestas-relacion/' + change['id'] + '/decisiones',
                        headers=headers, json={'decision': 'aprobar'})
    assert response.status_code == 409
    assert api.get('/api/v1/propuestas-relacion/' + change['id'], headers=headers).json()['estado'] == 'pendiente'
    current = api.get('/api/v1/relaciones/' + relation['id'], headers=headers).json()
    assert current['origen']['id'] == relation['origen']['id'] and current['version'] == relation['version']
