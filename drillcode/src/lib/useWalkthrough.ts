import { useEffect, useState } from 'react'
import { loadWalkthrough } from '@/lib/catalogue'

/** The walkthrough text for a problem, loaded on demand. `undefined` while loading or when there is none. */
export function useWalkthrough(slug: string, enabled = true): { text: string | undefined; loading: boolean } {
  const [state, setState] = useState<{ slug: string; text?: string } | null>(null)
  useEffect(() => {
    if (!enabled) return
    let cancelled = false
    loadWalkthrough(slug).then((text) => {
      if (!cancelled) setState({ slug, text })
    })
    return () => {
      cancelled = true
    }
  }, [slug, enabled])
  const ready = state?.slug === slug
  return { text: ready ? state.text : undefined, loading: enabled && !ready }
}
