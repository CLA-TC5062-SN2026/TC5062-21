export interface Usuario {
  id: string
  correo: string
  nombre: string
  rol: 'Administrador' | 'Editor' | 'Consulta'
  activo: boolean
  capasEditables: string[]
}
export interface Capa { id: string; nombre: string }
export interface TipoElemento { id: string; nombre: string; capaId: string }
export interface Elemento {
  id: string
  nombre: string
  tipoElemento: { id: string; nombre: string }
  capa: Capa
  estado: 'activo' | 'baja'
}
export interface ElementoDetalle extends Elemento {
  campos: { id: string; nombre: string; tipoDato: string; opciones: { id: string; etiqueta: string }[] }[]
  valores: { campoId: string; texto?: string; numero?: number; fecha?: string; opcionId?: string }[]
  autoria: { creadoEn: string; modificadoEn: string }
}
export interface Lista<T> { items: T[]; total: number }
export interface Pagina<T> extends Lista<T> { pagina: number; tamanoPagina: number }
export interface Acceso { accessToken: string; expiresIn: number; expiraEn: string; usuario: Usuario }
