import { useId } from 'react'
import type { InputHTMLAttributes } from 'react'
import styles from './ui.module.css'
type Props = InputHTMLAttributes<HTMLInputElement> & { label: string; error?: string; hint?: string }
export function Input({ label, error, hint, id: suppliedId, className = '', ...props }: Props) {
  const unique = useId()
  const id = suppliedId || unique
  const description = [props['aria-describedby'], error ? `${id}-error` : hint ? `${id}-hint` : ''].filter(Boolean).join(' ') || undefined
  return <div className={`${styles.field} ${className}`}>
    <label htmlFor={id}>{label}</label>
    <input {...props} id={id} aria-invalid={error ? true : undefined} aria-describedby={description} className={error ? styles.invalid : ''} />
    {error ? <p id={`${id}-error`} className={styles.fieldError}>{error}</p> : hint ? <p id={`${id}-hint`} className={styles.hint}>{hint}</p> : null}
  </div>
}
