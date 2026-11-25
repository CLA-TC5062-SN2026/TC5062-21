// @vitest-environment jsdom
import { afterEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import '@testing-library/jest-dom/vitest'
import { Button } from './Button'
import { Input } from './Input'
afterEach(cleanup)
it('un campo inválido conserva etiqueta, estado y explicación asociados', () => {
  render(<Input label="Correo" error="Escribe un correo válido." />)
  const input=screen.getByRole('textbox',{name:'Correo'})
  expect(input).toHaveAttribute('aria-invalid','true')
  expect(input).toHaveAccessibleDescription('Escribe un correo válido.')
})
it('dos campos sin id explícito reciben identificadores distintos', () => {
  render(<><Input label="Nombre" hint="Nombre reconocible"/><Input label="Descripción"/></>)
  const name=screen.getByRole('textbox',{name:'Nombre'})
  expect(name.id).not.toBe(screen.getByRole('textbox',{name:'Descripción'}).id)
  expect(name).toHaveAccessibleDescription('Nombre reconocible')
})
it('un botón cargando conserva su nombre y bloquea envíos duplicados', () => {
  const action=vi.fn()
  render(<Button loading onClick={action}>Guardar elemento</Button>)
  const button=screen.getByRole('button',{name:'Guardar elemento'})
  expect(button).toBeDisabled()
  expect(button).toHaveAttribute('aria-busy','true')
  fireEvent.click(button)
  expect(action).not.toHaveBeenCalled()
})
