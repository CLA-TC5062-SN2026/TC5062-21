import { useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useResource } from '../hooks/useResource'
import { Button } from '../components/Button'
import { Card } from '../components/Card'
import { Input } from '../components/Input'
import { ErrorState, Loading } from '../components/Feedback'
import { errorMessage } from '../services/client'
import { elementosService } from '../services/elementosService'
import { tiposService } from '../services/tiposService'
import { canEditLayer } from '../services/permissions'
import type { ElementoDetalle, TipoElemento, ValorCampo } from '../services/types'

function initialValues(element?: ElementoDetalle | null): Record<string, string> {
  return Object.fromEntries((element?.valores || []).map(value => [value.campoId,
    String(value.texto ?? value.numero ?? value.fecha ?? value.opcionId ?? '')]))
}

function ElementEditor({ kinds, element }: { kinds: TipoElemento[]; element?: ElementoDetalle | null }) {
  const navigate = useNavigate()
  const [kindId, setKindId] = useState(element?.tipoElemento.id || '')
  const [values, setValues] = useState(() => initialValues(element))
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [problem, setProblem] = useState('')
  const [saving, setSaving] = useState(false)
  const kind = kinds.find(item => item.id === kindId)
  const fields = [...(element?.campos || kind?.campos || [])].sort((a, b) =>
    Number(b.esBaseNombre) - Number(a.esBaseNombre) || a.nombre.localeCompare(b.nombre, 'es'))

  async function save(event: FormEvent) {
    event.preventDefault()
    if (saving) return
    const invalid: Record<string, string> = {}
    if (!kind) invalid.tipo = 'Selecciona un tipo de elemento.'
    const payload: ValorCampo[] = []
    for (const field of fields) {
      const value = values[field.id] || ''
      if (!value.trim()) {
        if (field.obligatorio) invalid[field.id] = field.nombre + ' es obligatorio.'
        else if (element?.valores.some(item => item.campoId === field.id)) payload.push({ campoId: field.id, vaciar: true })
        continue
      }
      if (field.tipoDato === 'numero') {
        const number = Number(value)
        if (!Number.isFinite(number)) invalid[field.id] = 'Escribe un número válido.'
        else payload.push({ campoId: field.id, numero: number })
      } else if (field.tipoDato === 'fecha') payload.push({ campoId: field.id, fecha: value })
      else if (field.tipoDato === 'seleccion') payload.push({ campoId: field.id, opcionId: value })
      else payload.push({ campoId: field.id, texto: value })
    }
    setErrors(invalid)
    setProblem('')
    if (Object.keys(invalid).length || !kind) {
      setProblem('Revisa los campos señalados. No se guardaron cambios.')
      return
    }
    setSaving(true)
    try {
      const result = element
        ? await elementosService.update(element.id, { valores: payload })
        : await elementosService.create({ tipoElementoId: kind.id, valores: payload })
      navigate('/elementos/' + result.id, { replace: true, state: { notice: element ? 'Cambios guardados. El identificador del elemento se conserva.' : 'Elemento creado y guardado.' } })
    } catch (error) { setProblem(errorMessage(error)) }
    finally { setSaving(false) }
  }

  return <Card title={element ? 'Modificar información' : 'Registrar elemento'}>
    <form className="element-form" onSubmit={save} noValidate aria-busy={saving}>
      <div className="select-field">
        <label htmlFor="tipo-elemento">Tipo de elemento</label>
        <select id="tipo-elemento" value={kindId} disabled={!!element || saving} aria-invalid={!!errors.tipo}
          aria-describedby={errors.tipo ? 'tipo-error' : undefined}
          onChange={event => { setKindId(event.target.value); setValues({}); setErrors({}); setProblem('') }}>
          <option value="">Selecciona un tipo</option>
          {kinds.map(item => <option key={item.id} value={item.id}>{item.nombre}</option>)}
        </select>
        {errors.tipo && <p className="field-problem" id="tipo-error">{errors.tipo}</p>}
      </div>
      {fields.map(field => field.tipoDato === 'seleccion'
        ? <div className="select-field" key={field.id}>
          <label htmlFor={field.id}>{field.nombre}{field.obligatorio ? ' *' : ''}</label>
          <select id={field.id} value={values[field.id] || ''} disabled={saving} required={field.obligatorio}
            aria-invalid={!!errors[field.id]} aria-describedby={errors[field.id] ? field.id + '-error' : undefined}
            onChange={event => { const value = event.target.value; setValues(current => ({ ...current, [field.id]: value })) }}>
            <option value="">Sin selección</option>
            {field.opciones.map(option => <option key={option.id} value={option.id}>{option.etiqueta}</option>)}
          </select>
          {errors[field.id] && <p className="field-problem" id={field.id + '-error'}>{errors[field.id]}</p>}
        </div>
        : <Input key={field.id} label={field.nombre + (field.obligatorio ? ' *' : '')} required={field.obligatorio}
          type={field.tipoDato === 'numero' ? 'number' : field.tipoDato === 'fecha' ? 'date' : 'text'}
          step={field.tipoDato === 'numero' ? 'any' : undefined} maxLength={field.esBaseNombre ? 500 : 10000}
          value={values[field.id] || ''} disabled={saving} error={errors[field.id]}
          onInput={field.tipoDato === 'fecha' ? event => { const value = event.currentTarget.value; setValues(current => ({ ...current, [field.id]: value })) } : undefined}
          onChange={event => { const value = event.target.value; setValues(current => ({ ...current, [field.id]: value })) }} />)}
      {problem && <p className="form-error" role="alert">{problem}</p>}
      <p className="form-hint">* Campo obligatorio. Los cambios se guardan juntos; si hay un error, no se aplica la operación.</p>
      <div className="button-row">
        <Button type="submit" loading={saving}>{element ? 'Guardar cambios' : 'Crear elemento'}</Button>
        <Button variant="secondary" disabled={saving} onClick={() => navigate(element ? '/elementos/' + element.id : '/elementos')}>Cancelar</Button>
      </div>
    </form>
  </Card>
}

export function ElementFormPage() {
  const { id } = useParams()
  const { user } = useAuth()
  const resource = useResource(id || 'nuevo', async signal => {
    const [kinds, element] = await Promise.all([
      tiposService.list(signal), id ? elementosService.detail(id, signal) : Promise.resolve(null),
    ])
    return { kinds: kinds.items, element }
  })
  const editable = resource.data?.kinds.filter(kind => canEditLayer(user, kind.capaId)) || []
  const permitted = !resource.data?.element || canEditLayer(user, resource.data.element.capa.id)
  return <>
    <div className="breadcrumbs"><Link to="/elementos">Elementos</Link><span>/</span><strong>{id ? 'Editar' : 'Nuevo elemento'}</strong></div>
    <div className="page-heading"><div><p className="eyebrow">INVENTARIO DE ARQUITECTURA</p><h1>{id ? 'Editar elemento' : 'Nuevo elemento'}</h1><p>Captura la información de acuerdo con los campos de su tipo.</p></div></div>
    {resource.loading ? <Loading /> : resource.error ? <ErrorState message={resource.error} retry={resource.retry} />
      : !editable.length || !permitted ? <p className="form-error" role="alert">Tu cuenta no tiene permiso para editar esta capa. Solicita una asignación al administrador.</p>
      : <ElementEditor key={id || 'nuevo'} kinds={editable} element={resource.data?.element} />}
  </>
}
