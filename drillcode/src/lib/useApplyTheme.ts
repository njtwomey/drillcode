import { useEffect } from 'react'
import { useStore } from '@/lib/store'

export function useApplyTheme() {
  const theme = useStore((s) => s.theme)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])
}
