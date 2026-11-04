import { createContext, useContext, useEffect, useRef, useState } from 'react'
import type { ReactNode } from 'react'
import { authService } from '../services/authService'
import { ApiError, errorMessage, isCanceled } from '../services/client'
import { getToken, SESSION_EXPIRED, setToken } from '../services/session'
import type { Usuario } from '../services/types'

type Auth = { user: Usuario | null; checking: boolean; expired: boolean; sessionError: string; retrySession: () => void; login: (correo: string, contrasena: string) => Promise<void>; logout: () => Promise<void> }
const AuthContext = createContext<Auth | null>(null)
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<Usuario | null>(null)
  const [checking, setChecking] = useState(!!getToken())
  const [expired, setExpired] = useState(false)
  const [sessionError, setSessionError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const generation = useRef(0)
  useEffect(() => {
    const controller = new AbortController()
    const clear = () => { generation.current++; setUser(null); setExpired(true); setChecking(false); setSessionError('') }
    window.addEventListener(SESSION_EXPIRED, clear)
    const current = generation.current
    if (getToken()) {
      setChecking(true); setSessionError('')
      authService.profile(controller.signal).then(profile => {
      if (generation.current === current) { setUser(profile); setSessionError('') }
    }).catch(error => {
      if (!isCanceled(error) && generation.current === current) setSessionError(errorMessage(error))
    }).finally(() => { if (!controller.signal.aborted) setChecking(false) })
    }
    else setChecking(false)
    return () => { controller.abort(); window.removeEventListener(SESSION_EXPIRED, clear) }
  }, [attempt])
  async function login(correo: string, contrasena: string) {
    const current = ++generation.current
    const result = await authService.login(correo, contrasena)
    if (!result.accessToken || !result.usuario?.id) throw new ApiError('La respuesta de acceso está incompleta.', 0, 'FORMATO')
    if (generation.current !== current) return
    setToken(result.accessToken); setUser(result.usuario); setExpired(false); setSessionError('')
  }
  async function logout() {
    generation.current++
    try { await authService.logout() } finally { setToken(null); setUser(null); setExpired(false); setSessionError('') }
  }
  return <AuthContext.Provider value={{ user, checking, expired, sessionError, retrySession: () => setAttempt(value => value + 1), login, logout }}>{children}</AuthContext.Provider>
}
export function useAuth() {
  const auth = useContext(AuthContext)
  if (!auth) throw new Error('Falta AuthProvider')
  return auth
}
