import { api } from './client'
import type { Elemento, ElementoDetalle, Pagina } from './types'
export type Filtros = { q?: string; capaId?: string; tipoElementoId?: string; pagina?: number }
export const elementosService = {
  list: (filters: Filtros = {}, signal?: AbortSignal) => {
    const query = new URLSearchParams()
    for (const [key, value] of Object.entries(filters)) if (value !== undefined && value !== '') query.set(key, String(value))
    return api<Pagina<Elemento>>(`/v1/elementos?${query}`, { signal })
  },
  detail: (id: string, signal?: AbortSignal) => api<ElementoDetalle>(`/v1/elementos/${encodeURIComponent(id)}`, { signal }),
}
