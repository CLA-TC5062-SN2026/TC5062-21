import { api } from './client'
import type { Lista, TipoElemento } from './types'
export const tiposService = { list: (signal?: AbortSignal) => api<Lista<TipoElemento>>('/v1/tipos-elemento', { signal }) }
