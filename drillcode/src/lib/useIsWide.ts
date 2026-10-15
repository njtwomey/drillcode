import { useSyncExternalStore } from 'react'

const QUERY = '(min-width: 1024px)'

/** True from the `lg` breakpoint up: where the three columns sit side by side and can be dragged. */
export function useIsWide(): boolean {
  return useSyncExternalStore(
    (notify) => {
      const media = window.matchMedia(QUERY)
      media.addEventListener('change', notify)
      return () => media.removeEventListener('change', notify)
    },
    () => window.matchMedia(QUERY).matches,
  )
}
