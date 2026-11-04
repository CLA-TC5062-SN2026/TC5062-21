import { api } from './client'
import type { Capa, Lista } from './types'
export const capasService = { list: (signal?: AbortSignal) => api<Lista<Capa>>('/v1/capas', { signal }) }
