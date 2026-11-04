import type { ButtonHTMLAttributes } from 'react'
import { LoaderCircle } from 'lucide-react'
import styles from './ui.module.css'
type Props = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary'; loading?: boolean }
export function Button({ variant = 'primary', loading = false, disabled, children, className = '', type = 'button', ...props }: Props) {
  return <button {...props} type={type} className={`${styles.button} ${styles[variant]} ${className}`} disabled={disabled || loading} aria-busy={loading || undefined}>
    {loading && <LoaderCircle size={17} className={styles.spin} aria-hidden="true" />}{children}
  </button>
}
