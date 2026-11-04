import { useEffect, useState } from 'react'
import { Check, ArrowRight, Layers3 } from 'lucide-react'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { Card } from '../components/Card'
export function ComponentsPage() {
  const [loading,setLoading]=useState(false)
  const [done,setDone]=useState(false)
  const [name,setName]=useState('')
  const [checked,setChecked]=useState(false)
  useEffect(()=>{
    if(!loading) return
    const timer=setTimeout(()=>{setLoading(false);setDone(true)},1200)
    return ()=>clearTimeout(timer)
  },[loading])
  return <><div className="breadcrumbs">Interfaz <span>/</span><strong>Componentes</strong></div><div className="page-heading"><div><p className="eyebrow">UNA INTERFAZ CONSISTENTE</p><h1>Componentes de UI</h1><p>Los cuatro componentes base y sus estados de interacción.</p></div><span className="version-tag">S07–S08 · A1</span></div>
    <div className="component-grid"><Card title="01 · Botón"><div className="component-body"><p>Variantes primaria, secundaria y estado de carga.</p><div className="button-row"><Button onClick={()=>{setDone(false);setLoading(true)}} loading={loading}>{loading?'Procesando…':done?'Listo':'Probar carga'}{!loading && (done?<Check size={16} aria-hidden="true"/>:<ArrowRight size={16} aria-hidden="true"/>)}</Button><Button variant="secondary" onClick={()=>{setDone(false);setLoading(false)}}>Restablecer</Button></div><p role="status" className="component-caption">{done?'Demostración completada. Puedes volver a probarla.':'La carga de esta demostración es simulada; no envía datos.'}</p></div></Card>
    <Card title="02 · Campo de entrada"><div className="component-body"><p>Etiqueta visible, descripción y validación asociada al campo.</p><form noValidate onSubmit={event=>{event.preventDefault();setChecked(true)}}><Input label="Nombre del elemento" value={name} onChange={event=>{setName(event.target.value);setChecked(false)}} placeholder="Por ejemplo, Gestión de clientes" error={checked&&!name.trim()?'El nombre es obligatorio.':undefined} hint="Usa un nombre claro y reconocible." required /><Button variant="secondary" type="submit">Validar campo</Button><p className="component-caption" role="status">{checked&&name.trim()?'El nombre es válido.':''}</p></form></div></Card>
    <Card title="03 · Tarjeta"><div className="component-body"><p>Contenedor para agrupar información y acciones relacionadas.</p><Card className="sample-card"><span className="stat-icon"><Layers3 aria-hidden="true" size={20}/></span><h3>Capa de negocio</h3><p>Una perspectiva para organizar objetivos, capacidades y procesos.</p></Card></div></Card>
    <Card title="04 · Barra de navegación"><div className="component-body"><p>La navegación de esta página es el componente reutilizable del proyecto.</p><ul className="plain-list"><li>Sin sesión: acceso al login y a esta galería.</li><li>Con sesión: panel, inventario e identidad del usuario.</li><li>En pantalla pequeña: menú desplegable con estado anunciado.</li></ul><p className="component-caption">Puedes recorrer enlaces y botones con Tab y activarlos con el teclado.</p></div></Card></div>
  </>
}
