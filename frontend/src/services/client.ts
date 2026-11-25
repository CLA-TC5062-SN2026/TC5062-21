import { getToken, SESSION_EXPIRED, setToken } from './session'

export class ApiError extends Error {
  readonly status: number
  readonly code: string
  constructor(message: string, status = 0, code = 'RED') {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
  }
}
type Options = { method?: string; body?: unknown; signal?: AbortSignal; auth?: boolean }
type Config = { baseUrl: string; token?: () => string | null; onUnauthorized?: (token: string) => void; timeout?: number }

// Una sola frontera HTTP: URL, JWT, formato de respuesta, red y vencimiento.
export function createApiClient({ baseUrl, token = getToken, onUnauthorized, timeout = 12000 }: Config) {
  return async function request<T>(path: string, options: Options = {}): Promise<T> {
    const bearer = options.auth === false ? null : token()
    const controller = new AbortController()
    const cancel = () => controller.abort()
    if (options.signal?.aborted) controller.abort()
    else options.signal?.addEventListener('abort', cancel, { once: true })
    const timer = setTimeout(cancel, timeout)
    try {
      const headers: Record<string, string> = { Accept: 'application/json' }
      if (bearer) headers.Authorization = `Bearer ${bearer}`
      if (options.body !== undefined) headers['Content-Type'] = 'application/json'
      const response = await fetch(`${baseUrl.replace(/\/$/, '')}/${path.replace(/^\//, '')}`, {
        method: options.method || 'GET', headers,
        body: options.body === undefined ? undefined : JSON.stringify(options.body),
        credentials: 'omit', signal: controller.signal,
      })
      const data = await response.json().catch(() => null)
      if (!response.ok) {
        if (response.status === 401 && bearer) onUnauthorized?.(bearer)
        const fallback: Record<number, string> = {
          401: options.auth === false ? 'El correo o la contraseña no son correctos.' : 'Tu sesión terminó. Inicia sesión de nuevo.',
          403: 'Tu cuenta no tiene permiso para realizar esta acción.',
          404: 'No encontramos el recurso solicitado.',
          422: 'Revisa los datos e inténtalo de nuevo.',
          429: 'Hay demasiadas solicitudes. Espera un momento e inténtalo de nuevo.',
          500: 'El servicio encontró un problema al procesar la solicitud. Inténtalo de nuevo.',
          503: 'El servicio no está disponible en este momento. Inténtalo de nuevo.',
        }
        // La sesión y los fallos internos usan mensajes propios; el backend no expone trazas.
        const message = response.status >= 500 && data === null
          ? 'No pudimos comunicarnos con el servicio. Inténtalo de nuevo en un momento.'
          : response.status === 401 || response.status >= 500
          ? fallback[response.status] || 'No pudimos completar la solicitud. Inténtalo de nuevo.'
          : typeof data?.mensaje === 'string' ? data.mensaje : fallback[response.status] || 'No pudimos completar la solicitud.'
        throw new ApiError(message, response.status, data?.codigo || 'HTTP')
      }
      if (data === null) throw new ApiError('El servicio devolvió una respuesta que no podemos interpretar.', response.status, 'FORMATO')
      return data as T
    } catch (error) {
      if (error instanceof ApiError) throw error
      if (options.signal?.aborted) throw new DOMException('Solicitud cancelada', 'AbortError')
      if (controller.signal.aborted) throw new ApiError('El servicio tardó demasiado en responder. Inténtalo de nuevo.', 0, 'TIEMPO_AGOTADO')
      throw new ApiError('No pudimos conectar con el servicio. Revisa tu conexión e inténtalo de nuevo.')
    } finally {
      clearTimeout(timer)
      options.signal?.removeEventListener('abort', cancel)
    }
  }
}
export const api = createApiClient({
  baseUrl: import.meta.env.VITE_API_URL || '/api',
  onUnauthorized: (expiredToken) => {
    // Una respuesta antigua no debe cerrar una sesión iniciada después.
    if (getToken() !== expiredToken) return
    setToken(null)
    window.dispatchEvent(new Event(SESSION_EXPIRED))
  },
})
export const errorMessage = (error: unknown) => error instanceof ApiError ? error.message : 'Ocurrió un problema. Inténtalo de nuevo.'
export const isCanceled = (error: unknown) => error instanceof DOMException && error.name === 'AbortError'
