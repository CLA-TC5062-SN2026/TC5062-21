import { Link, useParams } from 'react-router-dom'
import { ArrowLeft, Box, CalendarDays } from 'lucide-react'
import { Card } from '../components/Card'
import { Loading, ErrorState } from '../components/Feedback'
import { typeClass } from '../components/ElementsTable'
import { useResource } from '../hooks/useResource'
import { elementosService } from '../services/elementosService'
export function DetailPage() {
  const { id = '' } = useParams()
  const { data, loading, error, retry } = useResource(id, signal=>elementosService.detail(id,signal))
  return <><div className="breadcrumbs"><Link to="/elementos">Elementos</Link><span>/</span><strong>Detalle del elemento</strong></div><Link className="back-link" to="/elementos"><ArrowLeft size={16} aria-hidden="true" /> Volver al inventario</Link>
    {loading ? <Loading /> : error ? <ErrorState message={error} retry={retry} /> : data && <>
      <div className="detail-heading"><span className={`element-icon large ${typeClass(data.tipoElemento.nombre)}`}><Box size={29} aria-hidden="true" /></span><div><p className="eyebrow">{data.tipoElemento.nombre} · {data.capa.nombre}</p><h1>{data.nombre}</h1><span className="status"><span aria-hidden="true" />{data.estado==='activo'?'Activo':'Baja'}</span></div></div>
      <Card title="Información del elemento"><dl className="detail-fields"><div><dt>Capa</dt><dd>{data.capa.nombre}</dd></div><div><dt>Tipo de elemento</dt><dd>{data.tipoElemento.nombre}</dd></div>{data.campos.map(c=>{
        const v=data.valores.find(value=>value.campoId===c.id)
        const value=v?.texto ?? v?.numero ?? v?.fecha ?? c.opciones.find(o=>o.id===v?.opcionId)?.etiqueta ?? 'Sin información'
        return <div key={c.id}><dt>{c.nombre}</dt><dd>{String(value)}</dd></div>
      })}</dl></Card><p className="inventory-note"><CalendarDays size={14} aria-hidden="true" /> Última modificación: {new Date(data.autoria.modificadoEn).toLocaleString('es-MX',{dateStyle:'medium',timeStyle:'short'})}</p>
    </>}
  </>
}
