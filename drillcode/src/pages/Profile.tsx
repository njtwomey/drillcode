import { Link } from 'react-router'
import { bySlug } from '@/lib/catalogue'
import { currentStreak, formatAgo, solveStats } from '@/lib/stats'
import { useState } from 'react'
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { problems, TOPICS } from '@/lib/catalogue'
import { formatDuration } from '@/lib/format'
import { useStore } from '@/lib/store'
import type { Problem } from '@/lib/types'

function Row({ label, list, done }: { label: string; list: Problem[]; done: Record<string, true> }) {
  const n = list.filter((p) => done[p.slug]).length
  const pct = list.length ? Math.round((100 * n) / list.length) : 0
  return (
    <TableRow>
      <TableCell className="w-48">{label}</TableCell>
      <TableCell className="w-24 tabular-nums">{n} / {list.length}</TableCell>
      <TableCell><Progress value={pct} className="h-2" /></TableCell>
      <TableCell className="w-14 text-right tabular-nums text-muted-foreground">{pct}%</TableCell>
    </TableRow>
  )
}

function CompletionTable({ title, rows, done }: { title: string; rows: [string, Problem[]][]; done: Record<string, true> }) {
  return (
    <section className="space-y-2">
      <h2 className="text-sm font-medium">{title}</h2>
      <Table className="text-sm">
        <TableHeader>
          <TableRow>
            <TableHead>{title.replace('Completion by ', '')}</TableHead>
            <TableHead>Done</TableHead>
            <TableHead>Progress</TableHead>
            <TableHead className="text-right">%</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>{rows.map(([label, list]) => <Row key={label} label={label} list={list} done={done} />)}</TableBody>
      </Table>
    </section>
  )
}

function SolveList({ title, rows, detail }: { title: string; rows: [string, { count: number; last: number }][]; detail: (s: { count: number; last: number }) => string }) {
  return (
    <div className="space-y-2">
      <h3 className="text-xs font-semibold text-muted-foreground">{title}</h3>
      <ul className="divide-y rounded-md border text-sm">
        {rows.map(([slug, st]) => (
          <li key={slug}>
            <Link to={`/p/${slug}`} className="flex items-center justify-between gap-3 px-3 py-2 hover:bg-muted/50">
              <span className="truncate font-medium">{bySlug.get(slug)!.title}</span>
              <span className="shrink-0 text-xs text-muted-foreground">{detail(st)}</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

export function Profile() {
  const done = useStore((s) => s.done)
  const history = useStore((s) => s.practiceHistory)
  const resetProgress = useStore((s) => s.resetProgress)
  const solves = useStore((s) => s.solves)
  const [confirm, setConfirm] = useState(false)

  const byDifficulty: [string, Problem[]][] = (['easy', 'medium', 'hard'] as const).map((d) => [
    d[0].toUpperCase() + d.slice(1),
    problems.filter((p) => p.difficulty === d),
  ])
  const byTopic: [string, Problem[]][] = TOPICS.map((t) => [t, problems.filter((p) => p.topic === t)])
  const totalDone = problems.filter((p) => done[p.slug]).length
  const blind = problems.filter((p) => p.blind75)

  const stats = solveStats(solves)
  const weekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000
  const entries = [...stats.entries()].filter(([slug]) => bySlug.has(slug))
  const mostSolved = [...entries].sort((a, b) => b[1].count - a[1].count || b[1].last - a[1].last).slice(0, 8)
  const longestAgo = [...entries].sort((a, b) => a[1].last - b[1].last).slice(0, 8)

  return (
    <div className="mx-auto max-w-4xl space-y-8">
      <section className="space-y-2">
        <h1 className="text-xl font-semibold">Profile</h1>
        <p className="text-sm text-muted-foreground">
          Everything here is stored in this browser only. {totalDone} of {problems.length} problems done.
        </p>
        <Progress value={(100 * totalDone) / problems.length} className="h-2.5" />
      </section>

      <section className="space-y-3">
        <h2 className="text-sm font-medium">Statistics</h2>
        <div className="grid grid-cols-2 gap-3 md:grid-cols-4">
          {[
            ['Total solves', solves.length],
            ['Different problems solved', stats.size],
            ['Solves in the last 7 days', solves.filter((e) => e.at >= weekAgo).length],
            ['Day streak', currentStreak(solves)],
          ].map(([label, value]) => (
            <div key={label} className="rounded-xl border bg-card p-4 shadow-xs">
              <div className="text-2xl font-semibold tabular-nums">{value}</div>
              <div className="text-xs text-muted-foreground">{label}</div>
            </div>
          ))}
        </div>
        <p className="text-xs text-muted-foreground">
          A solve is counted each time every test passes in Practice, or in Implement mode (once per visit). Ticking Done by hand does not count, so problems you ticked earlier show no solves until you do them again.
        </p>
        {entries.length > 0 && (
          <div className="grid gap-6 md:grid-cols-2">
            <SolveList title="Most solved" rows={mostSolved} detail={(s) => `${s.count}× · last ${formatAgo(s.last)}`} />
            <SolveList title="Longest since you solved it (worth a review)" rows={longestAgo} detail={(s) => formatAgo(s.last)} />
          </div>
        )}
      </section>

      <div className="grid gap-8 md:grid-cols-2">
        <CompletionTable title="Completion by difficulty" rows={byDifficulty} done={done} />
        <CompletionTable title="Completion by set" rows={[['Blind 75', blind], ['Everything else', problems.filter((p) => !p.blind75)]]} done={done} />
      </div>
      <CompletionTable title="Completion by topic" rows={byTopic} done={done} />

      <section className="space-y-2">
        <h2 className="text-sm font-medium">Practice sessions</h2>
        {history.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No finished sessions yet. <Link to="/practice" className="underline">Start a practice session</Link>.
          </p>
        ) : (
          <Table className="text-sm">
            <TableHeader>
              <TableRow><TableHead>Finished</TableHead><TableHead>Solved</TableHead><TableHead>Time on solved problems</TableHead></TableRow>
            </TableHeader>
            <TableBody>
              {history.map((r) => (
                <TableRow key={r.finishedAt}>
                  <TableCell>{new Date(r.finishedAt).toLocaleString()}</TableCell>
                  <TableCell>{r.passed} of {r.total}</TableCell>
                  <TableCell>{formatDuration(r.seconds)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </section>

      <section className="space-y-2">
        <h2 className="text-sm font-medium">Reset</h2>
        <p className="text-sm text-muted-foreground">Clears every done tick, the solve statistics and the practice history. Your code drafts and custom test cases are kept.</p>
        <Button variant="outline" size="sm" onClick={() => setConfirm(true)}>Reset progress</Button>
      </section>

      <AlertDialog open={confirm} onOpenChange={setConfirm}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reset all progress?</AlertDialogTitle>
            <AlertDialogDescription>This removes {totalDone} done ticks and the practice history. It cannot be undone.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={resetProgress}>Reset</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
