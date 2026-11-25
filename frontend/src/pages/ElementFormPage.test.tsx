// @vitest-environment jsdom
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { ElementFormPage } from './ElementFormPage'
import { tiposService } from '../services/tiposService'
import { elementosService } from '../services/elementosService'
import { useAuth } from '../context/AuthContext'
import type { ElementoDetalle, TipoElemento, Usuario } from '../services/types'
vi.mock('../context/AuthContext', () => ({ useAuth: vi.fn() }))
const user: Usuario = { id: 'admin', correo: 'admin@equipo21.test', nombre: 'Administrador', rol: 'Administrador', activo: true, capasEditables: [] }
const kind: TipoElemento = { id: 'tipo', nombre: 'Proyecto', capaId: 'negocio', campos: [
  { id: 'nombre', nombre: 'Nombre', tipoDato: 'texto', obligatorio: true, esBaseNombre: true, opciones: [] },
  { id: 'monto', nombre: 'Presupuesto', tipoDato: 'numero', obligatorio: false, esBaseNombre: false, opciones: [] },
  { id: 'fecha', nombre: 'Fecha objetivo', tipoDato: 'fecha', obligatorio: false, esBaseNombre: false, opciones: [] },
  { id: 'estado', nombre: 'Etapa', tipoDato: 'seleccion', obligatorio: false, esBaseNombre: false, opciones: [{ id: 'planeado', etiqueta: 'Planeado' }] },
] }
const element: ElementoDetalle = { id: 'elemento', nombre: 'Proyecto inicial', tipoElemento: kind, capa: { id: 'negocio', nombre: 'Negocio' }, estado: 'activo', campos: kind.campos,
  valores: [{ campoId: 'nombre', texto: 'Proyecto inicial' }, { campoId: 'monto', numero: 1200 }],
  autoria: { creadorId: 'admin', ultimoModificadorId: 'admin', creadoEn: '2026-11-25T12:00:00Z', modificadoEn: '2026-11-25T12:00:00Z' } }
beforeEach(() => {
  vi.mocked(useAuth).mockReturnValue({ user } as ReturnType<typeof useAuth>)
  vi.spyOn(tiposService, 'list').mockResolvedValue({ items: [kind], total: 1 })
  vi.spyOn(elementosService, 'create').mockResolvedValue(element)
  vi.spyOn(elementosService, 'update').mockResolvedValue(element)
  vi.spyOn(elementosService, 'detail').mockResolvedValue(element)
})
afterEach(() => { cleanup(); vi.restoreAllMocks() })
function open(edit = false) {
  render(<MemoryRouter initialEntries={[edit ? '/elementos/elemento/editar' : '/elementos/nuevo']}><Routes>
    <Route path="/elementos/nuevo" element={<ElementFormPage />} /><Route path="/elementos/:id/editar" element={<ElementFormPage />} />
    <Route path="/elementos/:id" element={<p>Detalle guardado</p>} />
  </Routes></MemoryRouter>)
}
async function chooseType() {
  fireEvent.change(await screen.findByLabelText('Tipo de elemento'), { target: { value: 'tipo' } })
}
it('impide guardar un nombre obligatorio vacío sin llamar a la API', async () => {
  open(); await chooseType()
  fireEvent.click(screen.getByRole('button', { name: 'Crear elemento' }))
  expect(await screen.findByText('Nombre es obligatorio.')).toBeVisible()
  expect(elementosService.create).not.toHaveBeenCalled()
})
it('crea con los cuatro tipos de campo y abre el detalle solo después de guardar', async () => {
  open(); await chooseType()
  fireEvent.change(screen.getByLabelText('Nombre *'), { target: { value: 'Atención digital' } })
  fireEvent.change(screen.getByLabelText('Presupuesto'), { target: { value: '45000' } })
  fireEvent.input(screen.getByLabelText('Fecha objetivo'), { target: { value: '2026-12-10' } })
  fireEvent.change(screen.getByLabelText('Etapa'), { target: { value: 'planeado' } })
  fireEvent.click(screen.getByRole('button', { name: 'Crear elemento' }))
  await screen.findByText('Detalle guardado')
  expect(elementosService.create).toHaveBeenCalledWith({ tipoElementoId: 'tipo', valores: expect.arrayContaining([
    { campoId: 'nombre', texto: 'Atención digital' }, { campoId: 'monto', numero: 45000 },
    { campoId: 'fecha', fecha: '2026-12-10' }, { campoId: 'estado', opcionId: 'planeado' },
  ]) })
})
it('vacía un campo opcional en edición conservando el identificador', async () => {
  open(true)
  const number = await screen.findByLabelText('Presupuesto')
  fireEvent.change(number, { target: { value: '' } })
  fireEvent.click(screen.getByRole('button', { name: 'Guardar cambios' }))
  await screen.findByText('Detalle guardado')
  expect(elementosService.update).toHaveBeenCalledWith('elemento', { valores: expect.arrayContaining([{ campoId: 'monto', vaciar: true }]) })
  expect(elementosService.create).not.toHaveBeenCalled()
})
it('un rechazo del servidor conserva la captura y permite reintentar', async () => {
  vi.mocked(elementosService.create).mockRejectedValueOnce(new Error('rechazo'))
  open(); await chooseType()
  fireEvent.change(screen.getByLabelText('Nombre *'), { target: { value: 'Proyecto conservado' } })
  fireEvent.click(screen.getByRole('button', { name: 'Crear elemento' }))
  await screen.findByRole('alert')
  expect(screen.getByLabelText('Nombre *')).toHaveValue('Proyecto conservado')
  await waitFor(() => expect(screen.getByRole('button', { name: 'Crear elemento' })).toBeEnabled())
})
it('un editor sin permiso en la capa no recibe un formulario de escritura', async () => {
  vi.mocked(useAuth).mockReturnValue({ user: { ...user, rol: 'Editor', capasEditables: ['otra-capa'] } } as ReturnType<typeof useAuth>)
  open(true)
  expect(await screen.findByRole('alert')).toHaveTextContent('no tiene permiso')
  expect(screen.queryByRole('button', { name: 'Guardar cambios' })).toBeNull()
})
