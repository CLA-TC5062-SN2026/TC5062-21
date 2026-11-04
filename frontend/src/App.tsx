import { useEffect } from 'react'
import { BrowserRouter, Link, Navigate, Outlet, Route, Routes, useLocation } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { Navbar } from './components/Navbar'
import { Loading, ErrorState } from './components/Feedback'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { ElementsPage } from './pages/ElementsPage'
import { DetailPage } from './pages/DetailPage'
import { ComponentsPage } from './pages/ComponentsPage'
function FocusOnRoute() {
  const { pathname } = useLocation()
  useEffect(()=>{
    document.title = `${pathname.includes('elementos')?'Elementos':pathname==='/panel'?'Vista general':pathname==='/componentes'?'Componentes':'Acceso'} · Arquitectura Empresarial`
    document.getElementById('contenido')?.focus({preventScroll:true})
    window.scrollTo(0,0)
  },[pathname])
  return null
}
export function ProtectedRoute() {
  const {user,checking,sessionError,retrySession}=useAuth()
  const {pathname,search}=useLocation()
  if(checking) return <main id="contenido" tabIndex={-1}><Loading text="Comprobando tu sesión…" /></main>
  if(sessionError) return <main id="contenido" tabIndex={-1}><ErrorState message={sessionError} retry={retrySession}/></main>
  return user?<Outlet/>:<Navigate to="/login" state={{from:pathname+search}} replace/>
}
function Shell() {
  const {user}=useAuth()
  return <div className={user?'app-shell':'public-shell'}><Navbar/><main id="contenido" tabIndex={-1} className={user?'app-main':'public-main'}><div className="content-width"><Outlet/></div></main></div>
}
export default function App() {
  return <BrowserRouter><AuthProvider><a className="skip-link" href="#contenido">Saltar al contenido</a><FocusOnRoute/><Routes>
    <Route path="/login" element={<><Navbar/><LoginPage/></>}/>
    <Route element={<Shell/>}><Route path="/componentes" element={<ComponentsPage/>}/></Route>
    <Route element={<ProtectedRoute/>}><Route element={<Shell/>}><Route path="/panel" element={<DashboardPage/>}/><Route path="/elementos" element={<ElementsPage/>}/><Route path="/elementos/:id" element={<DetailPage/>}/></Route></Route>
    <Route path="/" element={<Navigate to="/panel" replace/>}/>
    <Route path="*" element={<Shell/>}><Route path="*" element={<div className="not-found"><p className="eyebrow">404</p><h1>No encontramos esta página</h1><p>Elige una sección para continuar.</p><Link className="text-link" to="/panel">Ir a la vista general</Link></div>}/></Route>
  </Routes></AuthProvider></BrowserRouter>
}
