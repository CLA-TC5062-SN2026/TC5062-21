import type { Usuario } from './types'

export const canEditLayer = (user: Usuario | null, layerId: string) =>
  !!user && (user.rol === 'Administrador' || (user.rol === 'Editor' && user.capasEditables.includes(layerId)))

export const canCreateElement = (user: Usuario | null) =>
  !!user && (user.rol === 'Administrador' || (user.rol === 'Editor' && user.capasEditables.length > 0))
