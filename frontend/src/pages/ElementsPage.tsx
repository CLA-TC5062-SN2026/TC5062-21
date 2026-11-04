import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Search, SlidersHorizontal, ArrowLeft, ArrowRight, Boxes, RefreshCw } from 'lucide-react'
import { useResource } from '../hooks/useResource'
import { elementosService } from '../services/elementosService'
import { capasService } from '../services/capasService'
import { tiposService } from '../services/tiposService'
import { Button } from '../components/Button'
import { Card } from '../components/Card'
import { Input } from '../components/Input'
import { Loading, ErrorState, EmptyState } from '../components/Feedback'
import { ElementsTable } from '../components/ElementsTable'
export function ElementsPage() {
  const [params, setParams] = useSearchParams()
  const key = params.toString()
  const [query, setQuery] = useState(params.get('q') || '')
  const [layer, setLayer] = useState(params.get('capaId') || '')
  const [type, setType] = useState(params.get('tipoElementoId') || '')
  useEffect(() => {
    const current = new URLSearchParams(key)
    setQuery(current.get('q') || ''); setLayer(current.get('capaId') || ''); setType(current.get('tipoElementoId') || '')
  }, [key])
  const page = Math.max(1, Number(params.get('pagina')) || 1)
  const catalogs = useResource('catalogs', async signal => {
    const [layers, types] = await Promise.all([capasService.list(signal), tiposService.list(signal)])
    return { layers, types }
  })
  const { data, loading, error, retry } = useResource(key, signal => elementosService.list({ q:params.get('q') || undefined, capaId:params.get('capaId') || undefined, tipoElementoId:params.get('tipoElementoId') || undefined, pagina:page }, signal))
  function apply(event: FormEvent) {
    event.preventDefault()
    const next = new URLSearchParams()
    if(query.trim()) next.set('q', query.trim())
    if(layer) next.set('capaId', layer)
    if(type) next.set('tipoElementoId', type)
    setParams(next)
  }
  function reset() { setQuery('');setLayer('');setType('');setParams({}) }
  function go(nextPage: number) { const next = new URLSearchParams(params); next.set('pagina',String(nextPage));setParams(next) }
  const filtered = !!(params.get('q') || params.get('capaId') || params.get('tipoElementoId'))
  return <>
    <div className="breadcrumbs">Espacio de trabajo <span>/</span> <strong>Elementos</strong></div>
    <div className="page-heading"><div><p className="eyebrow">EL INVENTARIO DE TU ORGANIZACIÓN</p><h1>Elementos de arquitectura</h1><p>Encuentra y consulta la información que conecta tu negocio.</p></div><Button variant="secondary" onClick={retry} disabled={loading}><RefreshCw size={15} aria-hidden="true" /> Actualizar</Button></div>
    <Card className="filter-card"><div className="filter-title"><SlidersHorizontal size={16} aria-hidden="true" /><h2>Explorar elementos</h2>{filtered && <button className="text-button" onClick={reset}>Limpiar filtros</button>}</div>
      <form className="filter-form" onSubmit={apply}>
        <Input label="Buscar por nombre" type="search" placeholder="Por ejemplo, atención digital" value={query} onChange={event=>setQuery(event.target.value)} maxLength={500} />
        <div className="select-field"><label htmlFor="capa">Capa</label><select id="capa" value={layer} onChange={event=>{setLayer(event.target.value);setType('')}} disabled={catalogs.loading}><option value="">Todas las capas</option>{catalogs.data?.layers.items.map(c=><option value={c.id} key={c.id}>{c.nombre}</option>)}</select></div>
        <div className="select-field"><label htmlFor="tipo">Tipo de elemento</label><select id="tipo" value={type} onChange={event=>setType(event.target.value)} disabled={catalogs.loading}><option value="">Todos los tipos</option>{catalogs.data?.types.items.filter(t=>!layer || t.capaId===layer).map(t=><option value={t.id} key={t.id}>{t.nombre}</option>)}</select></div>
        <Button type="submit" disabled={loading}><Search size={16} aria-hidden="true" /> Buscar</Button>
      </form>
      {catalogs.error && <div className="catalog-error" role="alert">No pudimos cargar los filtros. {catalogs.error} <button className="text-button" onClick={catalogs.retry}>Reintentar filtros</button></div>}
    </Card>
    <Card title="Inventario de elementos" action={<span className="result-count" role="status">{loading ? 'Consultando…' : data ? `${data.total} ${data.total===1?'elemento':'elementos'}` : 'Sin resultados disponibles'}</span>}>
      {loading ? <Loading text="Cargando elementos desde el servidor…" /> : error ? <ErrorState message={error} retry={retry} /> : data?.items.length ? <><ElementsTable items={data.items} /><div className="table-footer"><span>{(page-1)*data.tamanoPagina+1}–{Math.min(page*data.tamanoPagina,data.total)} de {data.total} elementos</span><div className="pagination"><Button variant="secondary" disabled={page<=1} onClick={()=>go(page-1)} aria-label="Página anterior"><ArrowLeft size={15} aria-hidden="true" /></Button><span>Página {page}</span><Button variant="secondary" disabled={page*data.tamanoPagina>=data.total} onClick={()=>go(page+1)} aria-label="Página siguiente"><ArrowRight size={15} aria-hidden="true" /></Button></div></div></> : <EmptyState reset={filtered?reset:undefined} />}
    </Card><p className="inventory-note"><Boxes size={14} aria-hidden="true" /> Consulta de elementos activos. Los datos de este entorno son ficticios.</p>
  </>
}
