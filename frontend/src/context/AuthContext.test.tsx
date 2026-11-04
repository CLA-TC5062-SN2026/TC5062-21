// @vitest-environment jsdom
import { afterEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { AuthProvider, useAuth } from './AuthContext'
import { authService } from '../services/authService'
import { ApiError } from '../services/client'
import { getToken, SESSION_EXPIRED, setToken } from '../services/session'
import type { Usuario } from '../services/types'
const profile:Usuario={id:'demo',correo:'demo@equipo21.test',nombre:'Consulta ficticia',rol:'Consulta',activo:true,capasEditables:[]}
function Probe(){const auth=useAuth();return <><p>{auth.checking?'Comprobando':auth.sessionError||auth.user?.nombre|| (auth.expired?'Sesión vencida':'Sin sesión')}</p><button onClick={auth.retrySession}>Reintentar</button></>}
afterEach(()=>{cleanup();setToken(null);vi.restoreAllMocks()})
it('una falla de red al recuperar la sesión permite reintentar sin borrar el token',async()=>{
  setToken('sesion-local')
  vi.spyOn(authService,'profile').mockRejectedValueOnce(new ApiError('Servicio no disponible',503)).mockResolvedValueOnce(profile)
  render(<AuthProvider><Probe/></AuthProvider>)
  await screen.findByText('Servicio no disponible')
  expect(getToken()).toBe('sesion-local')
  fireEvent.click(screen.getByRole('button',{name:'Reintentar'}))
  await screen.findByText('Consulta ficticia')
})
it('una respuesta 401 anunciada por el cliente elimina la identidad de la interfaz',async()=>{
  setToken('sesion-local')
  vi.spyOn(authService,'profile').mockResolvedValue(profile)
  render(<AuthProvider><Probe/></AuthProvider>)
  await screen.findByText('Consulta ficticia')
  setToken(null)
  window.dispatchEvent(new Event(SESSION_EXPIRED))
  await screen.findByText('Sesión vencida')
  expect(screen.queryByText('Consulta ficticia')).toBeNull()
})
