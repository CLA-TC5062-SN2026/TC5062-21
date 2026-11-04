import { Link } from 'react-router-dom'
import { ArrowUpRight, Box } from 'lucide-react'
import type { Elemento } from '../services/types'
export const typeClass = (type: string) => ({ Objetivo: 'goal', Proyecto: 'project', Capacidad: 'capability', Proceso: 'process', Aplicación: 'application' })[type] || 'other'
export function ElementsTable({ items }: { items: Elemento[] }) {
  return <div className="table-scroll" role="region" aria-label="Tabla de elementos" tabIndex={0}><table>
    <thead><tr><th scope="col">Elemento</th><th scope="col">Tipo</th><th scope="col">Capa</th><th scope="col">Estado</th><th scope="col"><span className="sr-only">Consultar</span></th></tr></thead>
    <tbody>{items.map(element => <tr key={element.id}>
      <td><Link to={`/elementos/${element.id}`} className="element-name"><span className={`element-icon ${typeClass(element.tipoElemento.nombre)}`}><Box size={17} aria-hidden="true" /></span>{element.nombre}</Link></td>
      <td><span className={`type-tag ${typeClass(element.tipoElemento.nombre)}`}>{element.tipoElemento.nombre}</span></td><td>{element.capa.nombre}</td>
      <td><span className={`status ${element.estado === 'baja' ? 'inactive' : ''}`}><span aria-hidden="true" />{element.estado === 'activo' ? 'Activo' : 'Baja'}</span></td>
      <td><Link to={`/elementos/${element.id}`} className="detail-link" aria-label={`Consultar ${element.nombre}`}><ArrowUpRight size={18} aria-hidden="true" /></Link></td>
    </tr>)}</tbody>
  </table></div>
}
