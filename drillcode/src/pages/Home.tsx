import { BookOpen, Dices, Flame, Footprints, Play, Pencil, RotateCcw, Sparkles } from 'lucide-react'
import { useMemo } from 'react'
import { Link, useNavigate } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { bySlug, hasWalkthrough, problems, TOPICS } from '@/lib/catalogue'
import { currentStreak, formatAgo, solveStats } from '@/lib/stats'
import { useStore } from '@/lib/store'
import { techniques } from '@/lib/techniques'
import type { Problem } from '@/lib/types'

const DAY = 24 * 60 * 60 * 1000

/** Same pick all day, a different one tomorrow. */
function dailyPick<T>(items: T[], salt: string): T | undefined {
  if (!items.length) return undefined
  const key = `${new Date().toDateString()}:${salt}`
  let hash = 0
  for (const ch of key) hash = (hash * 31 + ch.charCodeAt(0)) >>> 0
  return items[hash % items.length]
}

function Card({ title, icon, children }: { title: string; icon: React.ReactNode; children: React.ReactNode }) {
  return (
    <section className="flex flex-col gap-3 rounded-xl border bg-card p-5 shadow-xs">
      <h2 className="flex items-center gap-2 text-xs font-semibold tracking-wide text-muted-foreground uppercase">{icon}{title}</h2>
      {children}
    </section>
  )
}

/** Last 16 weeks of solves, one square per day (columns are weeks, rows are Sunday to Saturday). */
function Heatmap({ counts }: { counts: Map<string, number> }) {
  const weeks = 16
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const start = new Date(today.getTime() - (weeks * 7 - 1 + today.getDay()) * DAY)
  const cells = Array.from({ length: weeks * 7 }, (_, i) => new Date(start.getTime() + i * DAY))
  const level = (n: number) =>
    n === 0 ? 'bg-muted' : n === 1 ? 'bg-emerald-200 dark:bg-emerald-900' : n === 2 ? 'bg-emerald-400 dark:bg-emerald-700' : 'bg-emerald-600 dark:bg-emerald-500'
  return (
    <div className="grid grid-flow-col grid-rows-7 gap-1" aria-label="Solves per day, last 16 weeks">
      {cells.map((d) => {
        const key = d.toDateString()
        const n = counts.get(key) ?? 0
        return (
          <div
            key={key}
            title={`${n} solve${n === 1 ? '' : 's'} on ${d.toLocaleDateString()}`}
            className={`size-3.5 rounded-sm ${d > today ? 'opacity-0' : level(n)}`}
          />
        )
      })}
    </div>
  )
}

export function Home() {
  const navigate = useNavigate()
  const done = useStore((s) => s.done)
  const solves = useStore((s) => s.solves)
  const session = useStore((s) => s.practice)
  const walk = useStore((s) => s.walk)
  const setFilters = useStore((s) => s.setFilters)

  const stats = useMemo(() => solveStats(solves), [solves])
  const perDay = useMemo(() => {
    const m = new Map<string, number>()
    for (const e of solves) m.set(new Date(e.at).toDateString(), (m.get(new Date(e.at).toDateString()) ?? 0) + 1)
    return m
  }, [solves])

  const doneCount = problems.filter((p) => done[p.slug]).length
  const weekAgo = Date.now() - 7 * DAY
  const pickOfTheDay = dailyPick(problems.filter((p) => !done[p.slug]).length ? problems.filter((p) => !done[p.slug]) : problems, 'problem')
  const technique = dailyPick(techniques, 'technique')
  const reading = dailyPick(problems.filter((p) => hasWalkthrough(p.slug)), 'walkthrough')
  const review = [...stats.entries()].filter(([slug]) => bySlug.has(slug)).sort((a, b) => a[1].last - b[1].last).slice(0, 3)
  const unfinished = session && !session.finished ? session : null
  const topicCounts = useMemo(() => new Map(TOPICS.map((t) => [t, problems.filter((p) => p.topic === t || p.tags.includes(t)).length])), [])

  const randomProblem = () => navigate(`/p/${problems[Math.floor(Math.random() * problems.length)].slug}/view`)
  const showTopic = (topic: string) => {
    setFilters({ topics: [topic] })
    navigate('/problems')
  }
  const ProblemChips = ({ p }: { p: Problem }) => (
    <div className="flex flex-wrap items-center gap-1.5">
      <DifficultyBadge difficulty={p.difficulty} />
      <Badge variant="secondary">{p.topic}</Badge>
    </div>
  )

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <section className="space-y-5 py-6 text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">Drill the patterns, not just the problems.</h1>
        <p className="mx-auto max-w-2xl text-muted-foreground">
          {problems.length} problems with commented solutions, written-out walkthroughs and a Python runner in your browser,
          plus {techniques.length} technique pages for the moment a problem looks awkward.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <Button asChild size="lg"><Link to="/practice"><Play /> Start practising</Link></Button>
          <Button size="lg" variant="outline" onClick={randomProblem}><Dices /> Random problem</Button>
          <Button asChild size="lg" variant="ghost"><Link to="/problems">Browse all problems</Link></Button>
        </div>
      </section>

      {unfinished && (
        <div className="flex flex-wrap items-center gap-3 rounded-xl border bg-muted/40 p-4 text-sm">
          <RotateCcw className="size-4" />
          <span>Practice session in progress: problem {unfinished.index + 1} of {unfinished.slugs.length}.</span>
          <Button asChild size="sm" className="ml-auto"><Link to="/practice/session">Resume</Link></Button>
        </div>
      )}

      {walk && (
        <div className="flex flex-wrap items-center gap-3 rounded-xl border bg-muted/40 p-4 text-sm">
          <Footprints className="size-4" />
          <span>Random walk in progress: {walk.history.length} visited, {Object.values(walk.outcomes).filter((o) => o.status === 'passed').length} solved.</span>
          <Button asChild size="sm" className="ml-auto"><Link to="/practice/walk">Continue</Link></Button>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-3">
        <Card title="Problem of the day" icon={<Sparkles className="size-3.5" />}>
          {pickOfTheDay && (
            <>
              <div className="space-y-2">
                <Link to={`/p/${pickOfTheDay.slug}/view`} className="text-lg font-semibold hover:underline">{pickOfTheDay.number}. {pickOfTheDay.title}</Link>
                <ProblemChips p={pickOfTheDay} />
              </div>
              <div className="mt-auto flex gap-2">
                <Button asChild size="sm"><Link to={`/p/${pickOfTheDay.slug}/impl`}><Pencil /> Try it</Link></Button>
                <Button asChild size="sm" variant="outline"><Link to={`/p/${pickOfTheDay.slug}/read`}>Read first</Link></Button>
              </div>
            </>
          )}
        </Card>
        <Card title="Technique of the day" icon={<Sparkles className="size-3.5" />}>
          {technique && (
            <>
              <div className="space-y-2">
                <Link to={`/tips/${technique.slug}`} className="text-lg font-semibold hover:underline">{technique.title}</Link>
                <p className="text-sm text-muted-foreground">{technique.signal.replace(/`/g, '')}</p>
              </div>
              <Button asChild size="sm" variant="outline" className="mt-auto w-fit"><Link to={`/tips/${technique.slug}`}>Open the tip</Link></Button>
            </>
          )}
        </Card>
        <Card title="Today's walkthrough" icon={<BookOpen className="size-3.5" />}>
          {reading && (
            <>
              <div className="space-y-2">
                <Link to={`/p/${reading.slug}/read`} className="text-lg font-semibold hover:underline">{reading.number}. {reading.title}</Link>
                <ProblemChips p={reading} />
              </div>
              <Button asChild size="sm" variant="outline" className="mt-auto w-fit"><Link to={`/p/${reading.slug}/read`}><BookOpen /> Read it</Link></Button>
            </>
          )}
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-[1fr_auto]">
        <Card title="Your progress" icon={<Flame className="size-3.5" />}>
          <div className="space-y-1">
            <div className="flex items-baseline justify-between text-sm">
              <span><span className="text-2xl font-semibold tabular-nums">{doneCount}</span> of {problems.length} done</span>
              <span className="text-muted-foreground">{currentStreak(solves)} day streak · {solves.filter((e) => e.at >= weekAgo).length} solves this week</span>
            </div>
            <Progress value={(100 * doneCount) / problems.length} className="h-2" />
          </div>
          <div className="overflow-x-auto">
            <Heatmap counts={perDay} />
          </div>
          {solves.length === 0 && <p className="text-xs text-muted-foreground">Each time you pass every test in Practice or Implement, a square lights up here.</p>}
        </Card>
        {review.length > 0 && (
          <Card title="Worth a review" icon={<RotateCcw className="size-3.5" />}>
            <ul className="space-y-2 text-sm">
              {review.map(([slug, st]) => (
                <li key={slug} className="flex items-center justify-between gap-4">
                  <Link to={`/p/${slug}/impl`} className="font-medium hover:underline">{bySlug.get(slug)!.title}</Link>
                  <span className="text-xs text-muted-foreground">{formatAgo(st.last)}</span>
                </li>
              ))}
            </ul>
          </Card>
        )}
      </div>

      <section className="space-y-3">
        <h2 className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">Jump in by topic</h2>
        <div className="flex flex-wrap gap-2">
          {TOPICS.map((t) => (
            <button
              key={t}
              onClick={() => showTopic(t)}
              className="rounded-full border px-3 py-1 text-sm hover:bg-muted"
            >
              {t} <span className="text-muted-foreground">{topicCounts.get(t)}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  )
}
