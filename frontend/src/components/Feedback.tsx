import { AlertCircle, LoaderCircle, SearchX } from 'lucide-react'
import { Button } from './Button'
export function Loading({ text = 'Cargando información…' }: { text?: string }) {
  return <div className="feedback" role="status"><LoaderCircle className="spin" aria-hidden="true" /><p>{text}</p></div>
}
export function ErrorState({ message, retry }: { message: string; retry?: () => void }) {
  return <div className="feedback error-panel" role="alert"><AlertCircle aria-hidden="true" /><h2>No pudimos cargar la información</h2><p>{message}</p>{retry && <Button variant="secondary" onClick={retry}>Volver a intentar</Button>}</div>
}
export function EmptyState({ reset }: { reset?: () => void }) {
  return <div className="feedback"><SearchX aria-hidden="true" /><h2>No hay elementos para mostrar</h2><p>Prueba con otro nombre o cambia los filtros de búsqueda.</p>{reset && <Button variant="secondary" onClick={reset}>Limpiar filtros</Button>}</div>
}
