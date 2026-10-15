import { Moon, Sun } from 'lucide-react'
import { useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useStore } from '@/lib/store'

export function useApplyTheme() {
  const theme = useStore((s) => s.theme)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])
}

export function ThemeToggle() {
  const theme = useStore((s) => s.theme)
  const setTheme = useStore((s) => s.setTheme)
  return (
    <Button variant="ghost" size="icon" aria-label="Toggle theme" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      {theme === 'dark' ? <Sun /> : <Moon />}
    </Button>
  )
}
