import { HashRouter, Link, Route, Routes } from 'react-router'
import { ThemeToggle, useApplyTheme } from '@/components/ThemeToggle'
import { Landing } from '@/pages/Landing'
import { ProblemPage } from '@/pages/ProblemPage'

export default function App() {
  useApplyTheme()
  return (
    <HashRouter>
      <header className="flex h-11 items-center justify-between border-b px-4">
        <Link to="/" className="text-sm font-semibold">Interview workbench</Link>
        <ThemeToggle />
      </header>
      <main className="mx-auto max-w-7xl p-4">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/p/:slug" element={<ProblemPage />} />
        </Routes>
      </main>
    </HashRouter>
  )
}
