// @vitest-environment node
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createServer } from 'node:http'
import type { Server, IncomingMessage, ServerResponse } from 'node:http'
import type { AddressInfo } from 'node:net'
import { createApiClient } from './client'
let server: Server
let url: string
let handler: (req: IncomingMessage, res: ServerResponse) => void
beforeEach(async () => {
  handler = (_, res) => { res.setHeader('Content-Type', 'application/json'); res.end('{"items":[],"total":0}') }
  server = createServer((req, res) => handler(req, res))
  await new Promise<void>(resolve => server.listen(0, '127.0.0.1', resolve))
  url = `http://127.0.0.1:${(server.address() as AddressInfo).port}/api`
})
afterEach(async () => { server.closeAllConnections(); await new Promise<void>(resolve => server.close(() => resolve())) })
describe('Cliente HTTP con solicitudes reales a un servidor de prueba', () => {
  it('envía JWT y conserva el prefijo /api una sola vez', async () => {
    handler = (req,res) => { expect(req.url).toBe('/api/v1/elementos'); expect(req.headers.authorization).toBe('Bearer jwt-prueba'); res.end('{"total":5}') }
    const request=createApiClient({baseUrl:url+'/',token:()=> 'jwt-prueba'})
    expect(await request('/v1/elementos')).toEqual({total:5})
  })
  it('no envía JWT al login público y serializa las credenciales según contrato', async () => {
    handler = (req,res) => { expect(req.headers.authorization).toBeUndefined(); expect(req.headers['content-type']).toBe('application/json'); let body=''; req.on('data',chunk=>body+=chunk);req.on('end',()=>{expect(JSON.parse(body)).toEqual({correo:'demo@equipo21.test',contrasena:'ejemplo'});res.end('{"ok":true}')}) }
    await createApiClient({baseUrl:url,token:()=> 'jwt-anterior'})('/auth/login',{method:'POST',auth:false,body:{correo:'demo@equipo21.test',contrasena:'ejemplo'}})
  })
  it('notifica el 401 de una solicitud autenticada', async () => {
    const onUnauthorized=vi.fn()
    handler=(_,res)=>{res.statusCode=401;res.end('{"mensaje":"interno"}')}
    await expect(createApiClient({baseUrl:url,token:()=> 'jwt-vencido',onUnauthorized})('/auth/me')).rejects.toMatchObject({status:401,message:'Tu sesión terminó. Inicia sesión de nuevo.'})
    expect(onUnauthorized).toHaveBeenCalledWith('jwt-vencido')
  })
  it('un login rechazado no provoca un evento de sesión vencida', async () => {
    const onUnauthorized=vi.fn()
    handler=(_,res)=>{res.statusCode=401;res.end('{}')}
    await expect(createApiClient({baseUrl:url,onUnauthorized})('/auth/login',{auth:false})).rejects.toMatchObject({status:401})
    expect(onUnauthorized).not.toHaveBeenCalled()
  })
  it('traduce un 503 con HTML a un mensaje útil, sin mostrar el cuerpo del servidor', async () => {
    handler=(_,res)=>{res.statusCode=503;res.end('<html>traza interna</html>')}
    await expect(createApiClient({baseUrl:url})('/v1/elementos')).rejects.toMatchObject({status:503,message:'No pudimos comunicarnos con el servicio. Inténtalo de nuevo en un momento.'})
  })
  it('rechaza una respuesta exitosa que no contiene JSON', async () => {
    handler=(_,res)=>res.end('contenido inesperado')
    await expect(createApiClient({baseUrl:url})('/v1/elementos')).rejects.toMatchObject({code:'FORMATO'})
  })
  it('limita una solicitud que no responde', async () => {
    handler=()=>undefined
    await expect(createApiClient({baseUrl:url,timeout:30})('/v1/elementos')).rejects.toMatchObject({code:'TIEMPO_AGOTADO'})
  })
  it('distingue la cancelación al abandonar una vista', async () => {
    handler=()=>undefined
    const controller=new AbortController()
    const pending=createApiClient({baseUrl:url})('/v1/elementos',{signal:controller.signal})
    controller.abort()
    await expect(pending).rejects.toMatchObject({name:'AbortError'})
  })
  it('explica una conexión rechazada', async () => {
    await expect(createApiClient({baseUrl:'http://127.0.0.1:1'})('/v1/elementos')).rejects.toMatchObject({code:'RED'})
  })
})
