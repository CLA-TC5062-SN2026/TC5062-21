import { Link } from 'react-router-dom'
import { ArrowRight, ArrowUpRight, Boxes, Layers3, Shapes, RefreshCw, Network } from 'lucide-react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Loading, ErrorState, EmptyState } from '../components/Feedback'
import { ElementsTable } from '../components/ElementsTable'
import { useResource } from '../hooks/useResource'
import { elementosService } from '../services/elementosService'
import { capasService } from '../services/capasService'
import { tiposService } from '../services/tiposService'
export function DashboardPage() {
  const { data, loading, error, retry } = useResource('overview', async signal => {
    const [elements, layers, types] = await Promise.all([elementosService.list({}, signal), capasService.list(signal), tiposService.list(signal)])
    return { elements, layers, types }
  })
  return <>
    <div className="breadcrumbs">Espacio de trabajo <span>/</span> <strong>Vista general</strong></div>
    <div className="page-heading"><div><p className="eyebrow">EL PANORAMA COMPLETO</p><h1>Una visión conectada</h1><p>Conoce los elementos que componen la arquitectura de tu organización.</p></div><Button variant="secondary" onClick={retry} disabled={loading}><RefreshCw size={15} aria-hidden="true" /> Actualizar</Button></div>
    {loading ? <Loading text="Consultando tu espacio de trabajo…" /> : error ? <ErrorState message={error} retry={retry} /> : data && <>
      <div className="stats-grid">
        {[{label:'Elementos activos',value:data.elements.total,icon:Boxes,caption:'En el inventario de arquitectura'}, {label:'Capas configuradas',value:data.layers.total,icon:Layers3,caption:'Perspectivas de tu organización'}, {label:'Tipos de elemento',value:data.types.total,icon:Shapes,caption:'Definiciones en el modelo'}].map(({label,value,icon:Icon,caption}) => <Card className="stat-card" key={label}><div className="stat-top"><span>{label}</span><span className="stat-icon"><Icon size={18} aria-hidden="true" /></span></div><strong className="stat-number">{String(value).padStart(2,'0')}</strong><p>{caption}</p></Card>)}
      </div>
      <section className="explore-banner" aria-labelledby="explore-title"><div className="banner-icon"><Network size={32} strokeWidth={1.4} aria-hidden="true" /></div><div><span className="eyebrow">DE LA ESTRATEGIA A LA OPERACIÓN</span><h2 id="explore-title">Cada elemento tiene un lugar en tu organización.</h2><p>Explora objetivos, proyectos, capacidades, procesos y aplicaciones.</p></div><Link to="/elementos">Explorar inventario <ArrowUpRight size={17} aria-hidden="true" /></Link></section>
      <Card title="Tu inventario de arquitectura" action={<Link className="text-link" to="/elementos">Ver todos <ArrowRight size={15} aria-hidden="true" /></Link>}>
        {data.elements.items.length ? <ElementsTable items={data.elements.items.slice(0,5)} /> : <EmptyState />}
        <div className="table-footer"><span>Primeros {Math.min(data.elements.items.length,5)} de {data.elements.total} elementos activos</span><span>Ordenados por nombre</span></div>
      </Card>
      <div className="model-note"><span className="dot" /> Información consultada desde la API del proyecto <span>Modelo de demostración · Equipo 21</span></div>
    </>}
  </>
}
