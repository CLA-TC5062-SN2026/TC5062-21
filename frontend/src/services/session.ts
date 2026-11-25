const KEY = 'equipo21.accessToken'
let token: string | null = null
try { token = sessionStorage.getItem(KEY) } catch { /* El almacenamiento puede estar deshabilitado. */ }
export const getToken = () => token
export function setToken(value: string | null) {
  token = value
  try {
    if (value) sessionStorage.setItem(KEY, value)
    else sessionStorage.removeItem(KEY)
  } catch { /* La sesión sigue disponible en memoria durante esta visita. */ }
}
export const SESSION_EXPIRED = 'equipo21:sesion-expirada'
