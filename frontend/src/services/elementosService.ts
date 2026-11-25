import { api } from './client'
import type { Elemento, ElementoDetalle, Pagina, ValorCampo } from './types'
export type Filtros = { q?: string; capaId?: string; tipoElementoId?: string; pagina?: number; incluirBaja?: boolean }
export const elementosService = {
  list: (filters: Filtros = {}, signal?: AbortSignal) => {
    const query = new URLSearchParams()
    for (const [key, value] of Object.entries(filters)) if (value !== undefined && value !== '') query.set(key, String(value))
    return api<Pagina<Elemento>>(`/v1/elementos?${query}`, { signal })
  },
  detail: (id: string, signal?: AbortSignal, incluirBaja = false) => api<ElementoDetalle>(`/v1/elementos/${encodeURIComponent(id)}${incluirBaja ? '?incluirBaja=true' : ''}`, { signal }),
  create: (body: { tipoElementoId: string; valores: ValorCampo[] }) => api<ElementoDetalle>('/v1/elementos', { method: 'POST', body }),
  update: (id: string, body: { valores?: ValorCampo[]; estado?: 'activo' }) => api<ElementoDetalle>(`/v1/elementos/${encodeURIComponent(id)}`, { method: 'PATCH', body }),
  deactivate: (id: string) => api<ElementoDetalle>(`/v1/elementos/${encodeURIComponent(id)}`, { method: 'DELETE' }),
}
