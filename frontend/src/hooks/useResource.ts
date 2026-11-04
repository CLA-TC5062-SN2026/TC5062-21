import { useEffect, useRef, useState } from 'react'
import { errorMessage, isCanceled } from '../services/client'
export function useResource<T>(key: string, load: (signal: AbortSignal) => Promise<T>) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [attempt, setAttempt] = useState(0)
  const loader = useRef(load)
  useEffect(() => { loader.current = load }, [load])
  useEffect(() => {
    const controller = new AbortController()
    setLoading(true); setError(''); setData(null)
    loader.current(controller.signal).then(result => {
      if (!controller.signal.aborted) setData(result)
    }).catch(problem => {
      if (!controller.signal.aborted && !isCanceled(problem)) setError(errorMessage(problem))
    }).finally(() => { if (!controller.signal.aborted) setLoading(false) })
    return () => controller.abort()
  }, [key, attempt])
  return { data, error, loading, retry: () => setAttempt(value => value + 1) }
}
