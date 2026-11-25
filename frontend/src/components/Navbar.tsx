import { useRef, useState } from 'react'
import { NavLink, Link } from 'react-router-dom'
import { Layers3, LayoutDashboard, Boxes, Component, LogOut, Menu, X, ArrowUpRight, ShieldCheck } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import styles from './navbar.module.css'
export function Navbar() {
  const { user, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const toggleRef = useRef<HTMLButtonElement>(null)
  if (!user) return <header className={styles.publicNav}>
    <Link to="/login" className={styles.brand}><span className={styles.brandIcon}><Layers3 aria-hidden="true" size={23} /></span><span>Arquitectura<span className={styles.brandSub}>EMPRESARIAL</span></span></Link>
    <nav aria-label="Navegación principal"><Link to="/componentes">Componentes</Link><Link to="/login" className={styles.access}>Acceder <ArrowUpRight size={15} aria-hidden="true" /></Link></nav>
  </header>
  return <>
    <div className={styles.mobileBar}><Link to="/panel" className={styles.mobileBrand}><Layers3 size={22} aria-hidden="true" /> Arquitectura</Link><button ref={toggleRef} aria-expanded={open} aria-controls="sidebar-navigation" aria-label={open ? 'Cerrar menú' : 'Abrir menú'} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button></div>
    <aside className={`${styles.sidebar} ${open ? styles.open : ''}`} id="sidebar-navigation" onKeyDown={event => { if (event.key === 'Escape') { setOpen(false); toggleRef.current?.focus() } }}>
      <Link to="/panel" className={styles.brand} onClick={() => setOpen(false)}><span className={styles.brandIcon}><Layers3 size={23} aria-hidden="true" /></span><span>Arquitectura<span className={styles.brandSub}>EMPRESARIAL</span></span></Link>
      <div className={styles.workspace}><span className={styles.workspaceMark}>21</span><div>Espacio de trabajo<small>Equipo 21 · TC5062</small></div></div>
      <p className={styles.navLabel}>EXPLORAR</p>
      <nav aria-label="Navegación principal" onClick={() => setOpen(false)}>
        <NavLink to="/panel"><LayoutDashboard size={18} aria-hidden="true" /> Vista general</NavLink>
        <NavLink to="/elementos"><Boxes size={18} aria-hidden="true" /> Elementos</NavLink>
        <NavLink to="/componentes"><Component size={18} aria-hidden="true" /> Componentes de UI</NavLink>
      </nav>
      <div className={styles.sidebarBottom}><div className={styles.demoNote}><ShieldCheck size={19} aria-hidden="true" /><div>Entorno de demostración<small>Datos ficticios del proyecto</small></div></div>
        <div className={styles.user}><span className={styles.avatar}>{user.nombre.charAt(0).toUpperCase()}</span><div><strong>{user.nombre}</strong><small>{user.rol}</small></div><button onClick={() => { void logout().catch(() => undefined) }} aria-label="Cerrar sesión" title="Cerrar sesión"><LogOut size={18} aria-hidden="true" /></button></div>
      </div>
    </aside>
  </>
}
