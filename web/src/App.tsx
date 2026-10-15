import { HashRouter, Link, NavLink, Route, Routes } from 'react-router'
import { ThemeToggle } from '@/components/ThemeToggle'
import { useApplyTheme } from '@/lib/useApplyTheme'
import { Landing } from '@/pages/Landing'
import { Practice } from '@/pages/Practice'
import { PracticeSession } from '@/pages/PracticeSession'
import { ProblemPage } from '@/pages/ProblemPage'
import { Profile } from '@/pages/Profile'

const NAV = [
  { to: '/', label: 'Problems', end: true },
  { to: '/practice', label: 'Practice', end: false },
  { to: '/profile', label: 'Profile', end: false },
]

export default function App() {
  useApplyTheme()
  return (
    <HashRouter>
      <header className="flex h-12 items-center gap-6 border-b px-4">
        <Link to="/" className="text-sm font-semibold">Interview workbench</Link>
        <nav className="flex items-center gap-1 text-sm">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `rounded-md px-3 py-1.5 ${isActive ? 'bg-muted font-medium' : 'text-muted-foreground hover:text-foreground'}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto"><ThemeToggle /></div>
      </header>
      <main className="mx-auto w-full max-w-[1800px] p-4">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/p/:slug" element={<ProblemPage />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/practice/session" element={<PracticeSession />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </HashRouter>
  )
}
