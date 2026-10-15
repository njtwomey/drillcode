import { ArrowLeft, ArrowRight, Check, Dices, Flag, SlidersHorizontal } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router'
import { describeCriteria } from '@/components/CriteriaFields'
import { DifficultyBadge } from '@/components/badges'
import { PracticeProblem } from '@/components/PracticeProblem'
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { bySlug, problems } from '@/lib/catalogue'
import { matchesFilter } from '@/lib/filter'
import { formatDuration } from '@/lib/format'
import { seededShuffle, timeSeed } from '@/lib/random'
import { useStore } from '@/lib/store'
import type { CaseResult } from '@/lib/types'

function useElapsed(since: number) {
  const [now, setNow] = useState(Date.now())
  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(id)
  }, [])
  return Math.max(0, Math.round((now - since) / 1000))
}

/** A random walk through problems matching loose criteria: no count, no end, your place is kept. */
export function PracticeWalk() {
  const walk = useStore((s) => s.walk)
  if (!walk) return <Navigate to="/practice?tab=walk" replace />
  return <Walking />
}

function Walking() {
  const navigate = useNavigate()
  const walk = useStore((s) => s.walk)!
  const config = useStore((s) => s.walkConfig)
  const done = useStore((s) => s.done)
  const { walkGo, walkMove, walkAttempt, endWalk, markDone, recordSolve } = useStore()
  const [confirmEnd, setConfirmEnd] = useState(false)

  const slug = walk.history[walk.index]
  const problem = bySlug.get(slug)!
  const outcome = walk.outcomes[slug] ?? { status: 'pending' as const, attempts: 0, seconds: 0 }
  const elapsed = useElapsed(walk.problemStartedAt)
  const solved = Object.values(walk.outcomes).filter((o) => o.status === 'passed').length

  // Prefer problems not seen in this walk; once all have been seen, allow repeats (never the current one).
  const candidates = useMemo(() => {
    const pool = problems.filter((p) => matchesFilter(p, config, done))
    const seen = new Set(walk.history)
    const fresh = pool.filter((p) => !seen.has(p.slug))
    return fresh.length ? fresh : pool.filter((p) => p.slug !== slug)
  }, [config, done, walk.history, slug])

  function next() {
    const pick = seededShuffle(candidates, timeSeed())[0]
    if (pick) walkGo(pick.slug)
  }

  function onResults(results: CaseResult[]) {
    const passed = results.length > 0 && results.every((r) => r.status === 'pass')
    const firstPass = passed && outcome.status !== 'passed'
    walkAttempt(slug, passed)
    if (passed) markDone(slug)
    if (firstPass) recordSolve({ slug, source: 'practice', seconds: Math.round((Date.now() - walk.problemStartedAt) / 1000) })
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <div className="min-w-48 flex-1">
          <div className="text-sm font-medium">Random walk <span className="font-normal text-muted-foreground">· {walk.history.length} visited · {solved} solved</span></div>
          <div className="flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
            {describeCriteria(config)}
            <Link to="/practice?tab=walk" className="inline-flex items-center gap-1 underline"><SlidersHorizontal className="size-3" /> change</Link>
          </div>
        </div>
        <span className="text-sm tabular-nums text-muted-foreground">{formatDuration(outcome.status === 'passed' ? outcome.seconds : elapsed)}</span>
        <Button size="icon" variant="outline" aria-label="Previous problem in this walk" disabled={walk.index === 0} onClick={() => walkMove(-1)}><ArrowLeft /></Button>
        <Button size="icon" variant="outline" aria-label="Next problem in this walk" disabled={walk.index >= walk.history.length - 1} onClick={() => walkMove(1)}><ArrowRight /></Button>
        <Button size="sm" variant={outcome.status === 'passed' ? 'default' : 'outline'} onClick={next} disabled={candidates.length === 0}>
          {outcome.status === 'passed' ? <Check /> : <Dices />} {outcome.status === 'passed' ? 'Solved. Next random' : 'Skip to next random'}
        </Button>
        <Button size="sm" variant="ghost" onClick={() => setConfirmEnd(true)}><Flag /> End walk</Button>
      </div>
      {candidates.length === 0 && (
        <p className="rounded-md border p-3 text-sm text-muted-foreground">
          Nothing else matches these criteria. <Link to="/practice?tab=walk" className="underline">Change them</Link> to keep going.
        </p>
      )}

      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-semibold">{problem.number}. {problem.title}</h1>
        <DifficultyBadge difficulty={problem.difficulty} />
        {outcome.status === 'passed' && <Badge className="bg-green-600 text-white hover:bg-green-600">Solved</Badge>}
        {outcome.attempts > 0 && <span className="text-xs text-muted-foreground">{outcome.attempts} run{outcome.attempts === 1 ? '' : 's'}</span>}
      </div>

      <PracticeProblem key={slug} slug={slug} onResults={onResults} />

      <AlertDialog open={confirmEnd} onOpenChange={setConfirmEnd}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>End this walk?</AlertDialogTitle>
            <AlertDialogDescription>
              You have visited {walk.history.length} and solved {solved}. Ending forgets your place in the walk (your solves and done ticks are kept).
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Keep walking</AlertDialogCancel>
            <AlertDialogAction onClick={() => { endWalk(); navigate('/practice?tab=walk') }}>End walk</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
