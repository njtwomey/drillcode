import { Check, Flag, SkipForward } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, Navigate } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
import { PracticeProblem } from '@/components/PracticeProblem'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { bySlug } from '@/lib/catalogue'
import { formatDuration } from '@/lib/format'
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

export function PracticeSession() {
  const session = useStore((s) => s.practice)
  if (!session) return <Navigate to="/practice" replace />
  return session.finished ? <Summary /> : <Current />
}

function Current() {
  const session = useStore((s) => s.practice)!
  const { practiceAttempt, practiceAdvance, finishPractice, markDone, recordSolve } = useStore()
  const slug = session.slugs[session.index]
  const problem = bySlug.get(slug)!
  const outcome = session.outcomes[slug]
  const elapsed = useElapsed(session.problemStartedAt)
  const last = session.index === session.slugs.length - 1

  function onResults(results: CaseResult[]) {
    const passed = results.length > 0 && results.every((r) => r.status === 'pass')
    const firstPass = passed && outcome.status !== 'passed'
    practiceAttempt(slug, passed)
    if (passed) markDone(slug)
    if (firstPass) recordSolve({ slug, source: 'practice', seconds: Math.round((Date.now() - session.problemStartedAt) / 1000) })
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
        <div className="min-w-48 flex-1 space-y-1">
          <div className="text-xs text-muted-foreground">Problem {session.index + 1} of {session.slugs.length}</div>
          <Progress value={(100 * session.index) / session.slugs.length} className="h-2" />
        </div>
        <span className="text-sm tabular-nums text-muted-foreground">{formatDuration(outcome.status === 'passed' ? outcome.seconds : elapsed)}</span>
        {outcome.status === 'passed' ? (
          <Button size="sm" onClick={() => practiceAdvance(false)}>
            <Check /> {last ? 'Finish session' : 'Next problem'}
          </Button>
        ) : (
          <Button size="sm" variant="outline" onClick={() => practiceAdvance(true)}>
            <SkipForward /> {last ? 'Skip and finish' : 'Skip'}
          </Button>
        )}
        <Button size="sm" variant="ghost" onClick={finishPractice}><Flag /> End session</Button>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-semibold">{problem.number}. {problem.title}</h1>
        <DifficultyBadge difficulty={problem.difficulty} />
        {outcome.status === 'passed' && <Badge className="bg-green-600 text-white hover:bg-green-600">Solved</Badge>}
        {outcome.attempts > 0 && <span className="text-xs text-muted-foreground">{outcome.attempts} run{outcome.attempts === 1 ? '' : 's'}</span>}
      </div>

      <PracticeProblem key={slug} slug={slug} onResults={onResults} />
    </div>
  )
}

function Summary() {
  const session = useStore((s) => s.practice)!
  const discard = useStore((s) => s.discardPractice)
  const outcomes = session.slugs.map((slug) => ({ slug, ...session.outcomes[slug] }))
  const passed = outcomes.filter((o) => o.status === 'passed').length
  return (
    <div className="mx-auto max-w-3xl space-y-4">
      <h1 className="text-xl font-semibold">Session complete</h1>
      <p className="text-sm text-muted-foreground">You solved {passed} of {session.slugs.length}.</p>
      <Table className="text-sm">
        <TableHeader>
          <TableRow><TableHead>Problem</TableHead><TableHead>Result</TableHead><TableHead>Runs</TableHead><TableHead>Time</TableHead></TableRow>
        </TableHeader>
        <TableBody>
          {outcomes.map((o) => (
            <TableRow key={o.slug}>
              <TableCell><Link className="hover:underline" to={`/p/${o.slug}/view`}>{bySlug.get(o.slug)!.title}</Link></TableCell>
              <TableCell>{o.status === 'passed' ? 'Solved' : o.status === 'skipped' ? 'Skipped' : 'Not finished'}</TableCell>
              <TableCell>{o.attempts}</TableCell>
              <TableCell>{o.status === 'passed' ? formatDuration(o.seconds) : '–'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <div className="flex gap-2">
        <Button asChild><Link to="/practice" onClick={discard}>New session</Link></Button>
        <Button asChild variant="outline"><Link to="/profile">View profile</Link></Button>
      </div>
    </div>
  )
}
