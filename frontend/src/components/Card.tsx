import { useId } from 'react'
import type { HTMLAttributes, ReactNode } from 'react'
import styles from './ui.module.css'
type Props = Omit<HTMLAttributes<HTMLElement>, 'title'> & { title?: string; action?: ReactNode }
export function Card({ title, action, children, className = '', ...props }: Props) {
  const id = useId()
  return <section {...props} aria-labelledby={title ? id : props['aria-labelledby']} className={`${styles.card} ${className}`}>
    {title && <div className={styles.cardHead}><h2 id={id}>{title}</h2>{action}</div>}{children}
  </section>
}
