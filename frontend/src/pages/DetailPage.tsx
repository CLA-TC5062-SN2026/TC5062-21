import { useState } from 'react'
import { Link, useLocation, useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft, Box } from 'lucide-react'
import { Card } from '../components/Card'
import { Button } from '../components/Button'
import { Loading, ErrorState } from '../components/Feedback'
import { typeClass } from '../components/ElementsTable'
import { useAuth } from '../context/AuthContext'
import { useResource } from '../hooks/useResource'
import { errorMessage } from '../services/client'
import { elementosService } from '../services/elementosService'
import { canEditLayer } from '../services/permissions'

export function DetailPage() {
  const { id = '' } = useParams()
  const { user } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [confirming, setConfirming] = useState(false)
  const [busy, setBusy] = useState(false)
  const [problem, setProblem] = useState('')
  const [notice, setNotice] = useState<string>(location.state?.notice || '')
  const { data, loading, error, retry } = useResource(id, signal => elementosService.detail(id, signal, true))
  const editable = data && canEditLayer(user, data.capa.id)

  async function changeStatus() {
    if (!data || busy) return
    setBusy(true); setProblem(''); setNotice('')
    try {
      if (data.estado === 'activo') await elementosService.deactivate(id)
      else await elementosService.update(id, { estado: 'activo' })
      setNotice(data.estado === 'activo' ? 'Elemento dado de baja. Sus datos e historial se conservan.' : 'Elemento reactivado. Vuelve a aparecer en el inventario activo.')
      setConfirming(false)
      retry()
    } catch (error) { setProblem(errorMessage(error)) }
    finally { setBusy(false) }
  }

  return <>
    <div className="breadcrumbs"><Link to="/elementos">Elementos</Link><span>/</span><strong>Detalle del elemento</strong></div>
    <Link className="back-link" to="/elementos"><ArrowLeft size={16} aria-hidden="true" /> Volver al inventario</Link>
    {notice && <p className="notice" role="status">{notice}</p>}
    {problem && <p className="form-error" role="alert">{problem}</p>}
    {loading ? <Loading /> : error ? <ErrorState message={error} retry={retry} /> : data && <>
      <div className="detail-heading"><span className={'element-icon large ' + typeClass(data.tipoElemento.nombre)}><Box size={29} aria-hidden="true" /></span><div>
        <p className="eyebrow">{data.tipoElemento.nombre} · {data.capa.nombre}</p><h1>{data.nombre}</h1>
        <span className={'status ' + (data.estado === 'baja' ? 'inactive' : '')}><span aria-hidden="true" />{data.estado === 'activo' ? 'Activo' : 'Baja'}</span>
      </div></div>
      {editable && <div className="button-row detail-actions">
        {data.estado === 'activo' ? <>
          <Button variant="secondary" disabled={busy || confirming} onClick={() => navigate('/elementos/' + id + '/editar')}>Editar elemento</Button>
          <Button variant="secondary" disabled={busy || confirming} onClick={() => setConfirming(true)}>Dar de baja</Button>
        </> : <Button loading={busy} onClick={changeStatus}>Reactivar elemento</Button>}
      </div>}
      {confirming && <section className="confirmation" aria-label="Confirmación de baja">
        <h2>¿Dar de baja este elemento?</h2><p>Se ocultará del inventario activo y del mapa. Sus campos, relaciones e historial se conservarán.</p>
        <div className="button-row"><Button loading={busy} onClick={changeStatus}>Confirmar baja</Button><Button variant="secondary" disabled={busy} onClick={() => setConfirming(false)}>Cancelar baja</Button></div>
      </section>}
      <Card title="Información del elemento"><dl className="detail-fields">
        <div><dt>Identificador</dt><dd>{data.id}</dd></div><div><dt>Estado</dt><dd>{data.estado === 'activo' ? 'Activo' : 'Baja'}</dd></div>
        <div><dt>Capa</dt><dd>{data.capa.nombre}</dd></div><div><dt>Tipo de elemento</dt><dd>{data.tipoElemento.nombre}</dd></div>
        {data.campos.map(field => {
          const value = data.valores.find(item => item.campoId === field.id)
          const text = value?.texto ?? value?.numero ?? value?.fecha ?? field.opciones.find(option => option.id === value?.opcionId)?.etiqueta ?? 'Sin información'
          return <div key={field.id}><dt>{field.nombre}</dt><dd>{String(text)}</dd></div>
        })}
        <div><dt>Creado por (ID)</dt><dd>{data.autoria.creadorId}</dd></div><div><dt>Fecha de creación</dt><dd>{new Date(data.autoria.creadoEn).toLocaleString('es-MX')}</dd></div>
        <div><dt>Última modificación por (ID)</dt><dd>{data.autoria.ultimoModificadorId}</dd></div><div><dt>Fecha de modificación</dt><dd>{new Date(data.autoria.modificadoEn).toLocaleString('es-MX')}</dd></div>
      </dl></Card>
    </>}
  </>
}
