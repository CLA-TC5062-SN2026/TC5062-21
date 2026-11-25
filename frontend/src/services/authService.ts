import { api } from './client'
import type { Acceso, Usuario } from './types'
export const authService = {
  login: (correo: string, contrasena: string) => api<Acceso>('/auth/login', { method: 'POST', body: { correo, contrasena }, auth: false }),
  profile: (signal?: AbortSignal) => api<Usuario>('/auth/me', { signal }),
  logout: () => api('/v1/sesiones/actual', { method: 'DELETE' }),
}
