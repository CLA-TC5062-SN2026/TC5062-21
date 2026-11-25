export interface Usuario {
  id: string
  correo: string
  nombre: string
  rol: 'Administrador' | 'Editor' | 'Consulta'
  activo: boolean
  capasEditables: string[]
}
export interface Capa { id: string; nombre: string }
export interface Campo {
  id: string
  nombre: string
  tipoDato: 'texto' | 'numero' | 'fecha' | 'seleccion'
  obligatorio: boolean
  esBaseNombre: boolean
  opciones: { id: string; etiqueta: string }[]
}
export interface TipoElemento { id: string; nombre: string; capaId: string; campos: Campo[] }
export interface ValorCampo { campoId: string; texto?: string; numero?: number; fecha?: string; opcionId?: string; vaciar?: boolean }
export interface Elemento {
  id: string
  nombre: string
  tipoElemento: { id: string; nombre: string }
  capa: Capa
  estado: 'activo' | 'baja'
}
export interface ElementoDetalle extends Elemento {
  campos: Campo[]
  valores: ValorCampo[]
  autoria: { creadorId: string; creadoEn: string; ultimoModificadorId: string; modificadoEn: string }
}
export interface Lista<T> { items: T[]; total: number }
export interface Pagina<T> extends Lista<T> { pagina: number; tamanoPagina: number }
export interface Acceso { accessToken: string; expiresIn: number; expiraEn: string; usuario: Usuario }
