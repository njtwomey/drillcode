import { CircleUser } from 'lucide-react'
import { BrowserRouter, Link, Navigate, NavLink, Route, Routes, useParams } from 'react-router'
import { ThemeToggle } from '@/components/ThemeToggle'
import { useApplyTheme } from '@/lib/useApplyTheme'
import { Home } from '@/pages/Home'
import { Practice } from '@/pages/Practice'
import { PracticeSession } from '@/pages/PracticeSession'
import { PracticeWalk } from '@/pages/PracticeWalk'
import { ProblemPage } from '@/pages/ProblemPage'
import { Problems } from '@/pages/Problems'
import { Profile } from '@/pages/Profile'
import { TipPage } from '@/pages/TipPage'
import { Tips } from '@/pages/Tips'

const NAV = [
  { to: '/problems', label: 'Problems', end: false },
  { to: '/practice', label: 'Practice', end: false },
  { to: '/tips', label: 'Tips', end: false },
]

/** /p/:slug on its own is the solution view. */
function ToView() {
  const { slug } = useParams()
  return <Navigate to={`/p/${slug}/view`} replace />
}

export default function App() {
  useApplyTheme()
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL.replace(/\/$/, '')}>
      <header className="flex h-12 items-center gap-6 border-b px-4">
        <Link to="/" className="text-sm font-semibold">DrillCode</Link>
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
        <div className="ml-auto flex items-center gap-1">
          <NavLink
            to="/profile"
            aria-label="Profile"
            title="Profile: progress and practice history"
            className={({ isActive }) =>
              `inline-flex size-9 items-center justify-center rounded-md hover:bg-muted ${isActive ? 'bg-muted' : 'text-muted-foreground hover:text-foreground'}`
            }
          >
            <CircleUser className="size-5" />
          </NavLink>
          <ThemeToggle />
        </div>
      </header>
      <main className="mx-auto w-full max-w-[1800px] p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/problems" element={<Problems />} />
          <Route path="/p/:slug" element={<ToView />} />
          <Route path="/p/:slug/view" element={<ProblemPage mode="view" />} />
          <Route path="/p/:slug/impl" element={<ProblemPage mode="impl" />} />
          <Route path="/p/:slug/read" element={<ProblemPage mode="read" />} />
          <Route path="/practice" element={<Practice />} />
          <Route path="/practice/session" element={<PracticeSession />} />
          <Route path="/practice/walk" element={<PracticeWalk />} />
          <Route path="/tips" element={<Tips />} />
          <Route path="/tips/:slug" element={<TipPage />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
