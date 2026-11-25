import { useRef, useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { ArrowRight, ShieldCheck, Layers3, Network, CircleCheck, AlertCircle } from 'lucide-react'
import { Button } from '../components/Button'
import { Input } from '../components/Input'
import { useAuth } from '../context/AuthContext'
import { errorMessage } from '../services/client'
import styles from './login.module.css'
export function LoginPage() {
  const { user, login, expired } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [correo, setCorreo] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [errors, setErrors] = useState<{ correo?: string; password?: string }>({})
  const [error, setError] = useState('')
  const errorRef = useRef<HTMLDivElement>(null)
  if (user) return <Navigate to="/panel" replace />
  async function submit(event: FormEvent) {
    event.preventDefault()
    if (busy) return
    const next = {
      correo: !correo.trim() ? 'Escribe tu correo electrónico.' : !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo.trim()) ? 'Escribe un correo válido.' : undefined,
      password: !password ? 'Escribe tu contraseña.' : undefined,
    }
    setErrors(next); setError('')
    if (next.correo || next.password) { document.getElementById(next.correo ? 'correo' : 'contrasena')?.focus(); return }
    setBusy(true)
    try {
      await login(correo.trim(), password)
      const from = location.state?.from
      navigate(typeof from === 'string' && /^\/(panel|elementos)(\/|\?|$)/.test(from) ? from : '/panel', { replace: true })
    } catch (problem) {
      setError(errorMessage(problem)); setPassword('')
      requestAnimationFrame(() => errorRef.current?.focus())
    } finally { setBusy(false) }
  }
  return <main id="contenido" tabIndex={-1} className={styles.login}>
    <section className={styles.intro} aria-labelledby="intro-title"><div className={styles.eyebrow}><span /> CONECTA LA VISIÓN CON LA OPERACIÓN</div>
      <h1 id="intro-title">Tu organización,<br />en una sola <em>visión.</em></h1>
      <p className={styles.lead}>Explora los elementos que dan forma a tu negocio y descubre cómo se conectan entre sí.</p>
      <div className={styles.diagram} aria-label="Ilustración de las capas del modelo de arquitectura"><div className={styles.diagramTop}><span className={styles.layerIcon}><Layers3 size={19} aria-hidden="true" /></span><div><strong>Arquitectura empresarial</strong><small>Una perspectiva compartida</small></div><span className={styles.liveDot} /></div>
        <div className={styles.diagramLine} /><div className={styles.diagramNodes}>{['Negocio', 'Datos', 'Aplicaciones'].map((text, index) => <div key={text}><span>{String(index + 1).padStart(2, '0')}</span><strong>{text}</strong><small>Capa del modelo</small></div>)}</div>
        <div className={styles.diagramFoot}><Network size={14} aria-hidden="true" /> Elementos conectados. Decisiones informadas.<span>Ilustración</span></div>
      </div>
      <div className={styles.benefits}><span><CircleCheck size={15} aria-hidden="true" /> Información estructurada</span><span><CircleCheck size={15} aria-hidden="true" /> Acceso por roles</span></div>
    </section>
    <section className={styles.loginCard} aria-labelledby="login-title"><div className={styles.cardIcon}><ShieldCheck size={25} aria-hidden="true" /></div><p className={styles.kicker}>TU ESPACIO DE TRABAJO</p><h2 id="login-title">Bienvenido de nuevo</h2><p className={styles.description}>Ingresa para explorar la arquitectura de tu organización.</p>
      {expired && !error && <p className="notice" role="status">Tu sesión terminó. Inicia sesión para continuar.</p>}
      {error && <div ref={errorRef} tabIndex={-1} role="alert" className="form-error"><AlertCircle size={18} aria-hidden="true" /><span>{error}</span></div>}
      <form onSubmit={submit} noValidate className={styles.form}>
        <Input id="correo" label="Correo electrónico" type="email" autoComplete="username" placeholder="tu@organizacion.com" value={correo} onChange={event => setCorreo(event.target.value)} error={errors.correo} required disabled={busy} />
        <Input id="contrasena" label="Contraseña" type="password" autoComplete="current-password" placeholder="Escribe tu contraseña" value={password} onChange={event => setPassword(event.target.value)} error={errors.password} required disabled={busy} />
        <Button type="submit" loading={busy}>{busy ? 'Iniciando sesión…' : 'Iniciar sesión'}{!busy && <ArrowRight size={17} aria-hidden="true" />}</Button>
      </form><div className={styles.secure}><ShieldCheck size={14} aria-hidden="true" /> Acceso seguro a tu espacio de trabajo</div>
      <p className={styles.demo}>Proyecto académico · Equipo 21<br /><span>Entorno de demostración con datos ficticios</span></p>
    </section>
  </main>
}
