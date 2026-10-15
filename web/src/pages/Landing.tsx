import { ArrowDown, ArrowUp, ArrowUpDown, Check, ExternalLink, Play, Search, Shuffle, X } from 'lucide-react'
import { useMemo } from 'react'
import { Link, useNavigate } from 'react-router'
import { Chart } from '@/components/Chart'
import { DifficultyBadge } from '@/components/badges'
import { MultiSelect } from '@/components/MultiSelect'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { problems, TOPICS } from '@/lib/catalogue'
import { matchesFilter } from '@/lib/filter'
import { useStore, type SortKey } from '@/lib/store'
import type { Difficulty, Problem } from '@/lib/types'

const RANK: Record<Difficulty, number> = { easy: 0, medium: 1, hard: 2 }

const COLUMNS: { key: SortKey; label: string; className?: string }[] = [
  { key: 'done', label: 'Done', className: 'w-14' },
  { key: 'number', label: '#', className: 'w-16' },
  { key: 'title', label: 'Title' },
  { key: 'difficulty', label: 'Difficulty' },
  { key: 'topic', label: 'Topic' },
  { key: 'tags', label: 'Also uses' },
  { key: 'flags', label: 'Blind 75 / premium', className: 'w-40' },
]

function compare(key: SortKey, done: Record<string, true>) {
  return (a: Problem, b: Problem) => {
    const value = (p: Problem): number | string => {
      switch (key) {
        case 'done': return done[p.slug] ? 1 : 0
        case 'number': return p.number
        case 'title': return p.title.toLowerCase()
        case 'difficulty': return RANK[p.difficulty]
        case 'topic': return p.topic
        case 'tags': return p.tags.join(', ')
        case 'flags': return (p.blind75 ? 2 : 0) + (p.premium ? 1 : 0)
      }
    }
    const x = value(a)
    const y = value(b)
    const order = typeof x === 'string' ? x.localeCompare(y as string) : x - (y as number)
    return order || a.number - b.number
  }
}

export function Landing() {
  const navigate = useNavigate()
  const done = useStore((s) => s.done)
  const filters = useStore((s) => s.filters)
  const sort = useStore((s) => s.sort)
  const queue = useStore((s) => s.queue)
  const { toggleDone, setFilters, clearFilters, setSort, setQueue, clearQueue } = useStore()

  const filtered = useMemo(() => {
    const rows = problems.filter((p) => matchesFilter(p, filters) && !(filters.hideDone && done[p.slug]))
    if (!sort.key) return rows
    const sorted = [...rows].sort(compare(sort.key, done))
    return sort.dir === 'desc' ? sorted.reverse() : sorted
  }, [filters, done, sort])

  const doneInView = filtered.filter((p) => done[p.slug]).length
  const filtering =
    filters.search || filters.difficulties.length || filters.topics.length || filters.blind75Only || filters.hideDone

  function clickHeader(key: SortKey) {
    if (sort.key !== key) setSort({ key, dir: 'asc' })
    else if (sort.dir === 'asc') setSort({ key, dir: 'desc' })
    else setSort({ key: null, dir: 'asc' })
  }

  const chartOption = useMemo(() => {
    const topics = TOPICS.filter((t) => problems.some((p) => p.topic === t))
    const total = topics.map((t) => problems.filter((p) => p.topic === t).length)
    const doneByTopic = topics.map((t) => problems.filter((p) => p.topic === t && done[p.slug]).length)
    return {
      tooltip: { trigger: 'axis' as const },
      legend: { top: 0 },
      xAxis: { type: 'category' as const, data: topics, axisLabel: { rotate: 35, interval: 0 } },
      yAxis: { type: 'value' as const, minInterval: 1 },
      series: [
        { name: 'Done', type: 'bar' as const, stack: 'n', data: doneByTopic },
        { name: 'Remaining', type: 'bar' as const, stack: 'n', data: total.map((n, i) => n - doneByTopic[i]) },
      ],
    }
  }, [done])

  function shuffle() {
    const slugs = filtered.map((p) => p.slug)
    for (let i = slugs.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[slugs[i], slugs[j]] = [slugs[j], slugs[i]]
    }
    setQueue(slugs)
  }

  return (
    <div className="mx-auto max-w-7xl space-y-5">
      <section className="space-y-4 rounded-lg border p-4">
        <div className="grid items-end gap-3 md:grid-cols-[minmax(220px,1fr)_180px_220px]">
          <div className="space-y-1">
            <Label htmlFor="search" className="text-xs text-muted-foreground">Search</Label>
            <div className="relative">
              <Search className="absolute top-2 left-2.5 size-4 text-muted-foreground" />
              <Input
                id="search"
                className="h-8 pr-8 pl-8"
                placeholder="Title, number, topic or tag"
                value={filters.search}
                onChange={(e) => setFilters({ search: e.target.value })}
              />
              {filters.search && (
                <button className="absolute top-2 right-2 text-muted-foreground hover:text-foreground" aria-label="Clear search" onClick={() => setFilters({ search: '' })}>
                  <X className="size-4" />
                </button>
              )}
            </div>
          </div>
          <MultiSelect
            label="Difficulty"
            allLabel="Any difficulty"
            options={['easy', 'medium', 'hard'] as const}
            value={filters.difficulties}
            onChange={(difficulties) => setFilters({ difficulties })}
            display={(d) => d[0].toUpperCase() + d.slice(1)}
          />
          <MultiSelect
            label="Topic"
            allLabel="Any topic"
            options={TOPICS}
            value={filters.topics}
            onChange={(topics) => setFilters({ topics })}
            columns={2}
          />
        </div>
        <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm">
          <Label className="gap-2 font-normal">
            <Switch checked={filters.blind75Only} onCheckedChange={(c) => setFilters({ blind75Only: c })} />
            Only the Blind 75
          </Label>
          <Label className="gap-2 font-normal">
            <Switch checked={filters.hideDone} onCheckedChange={(c) => setFilters({ hideDone: c })} />
            Hide problems I’ve done
          </Label>
          {filtering ? (
            <Button variant="ghost" size="sm" onClick={clearFilters}><X /> Clear filters</Button>
          ) : null}
          <span className="ml-auto text-muted-foreground">
            Showing {filtered.length} of {problems.length} · {doneInView} done
          </span>
          <div className="flex items-center gap-2">
            <Button size="sm" variant="outline" onClick={shuffle} disabled={!filtered.length} title="Put the problems shown here in a random order, then step through them with the next and previous arrows">
              <Shuffle /> Shuffle these
            </Button>
            {queue.length > 0 && (
              <>
                <Button size="sm" onClick={() => navigate(`/p/${queue[0]}`)}><Play /> Start ({queue.length})</Button>
                <Button size="icon" variant="ghost" aria-label="Clear shuffled order" onClick={clearQueue}><X /></Button>
              </>
            )}
          </div>
        </div>
      </section>

      <Table className="text-sm">
        <TableHeader>
          <TableRow>
            {COLUMNS.map((c) => {
              const active = sort.key === c.key
              const Icon = !active ? ArrowUpDown : sort.dir === 'asc' ? ArrowUp : ArrowDown
              return (
                <TableHead key={c.key} className={c.className} aria-sort={active ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}>
                  <button className="inline-flex items-center gap-1 font-medium hover:text-foreground" onClick={() => clickHeader(c.key)}>
                    {c.label}
                    <Icon className={`size-3.5 ${active ? '' : 'opacity-40'}`} />
                  </button>
                </TableHead>
              )
            })}
            <TableHead className="w-8"><span className="sr-only">LeetCode</span></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((p) => (
            <TableRow key={p.slug} className={done[p.slug] ? 'opacity-60' : ''}>
              <TableCell>
                <Checkbox checked={!!done[p.slug]} onCheckedChange={() => toggleDone(p.slug)} aria-label={`Mark ${p.title} done`} />
              </TableCell>
              <TableCell className="text-muted-foreground">{p.number}</TableCell>
              <TableCell><Link to={`/p/${p.slug}`} className="font-medium hover:underline">{p.title}</Link></TableCell>
              <TableCell><DifficultyBadge difficulty={p.difficulty} /></TableCell>
              <TableCell><Badge variant="secondary">{p.topic}</Badge></TableCell>
              <TableCell className="space-x-1">{p.tags.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}</TableCell>
              <TableCell className="space-x-1">
                {p.blind75 && <Badge variant="outline" title="In the Blind 75"><Check className="size-3" />Blind 75</Badge>}
                {p.premium && <Badge variant="outline" title="Needs a LeetCode subscription">Premium</Badge>}
              </TableCell>
              <TableCell>
                <a href={p.leetcode} target="_blank" rel="noreferrer" aria-label={`Open ${p.title} on LeetCode`}>
                  <ExternalLink className="size-4 text-muted-foreground hover:text-foreground" />
                </a>
              </TableCell>
            </TableRow>
          ))}
          {filtered.length === 0 && (
            <TableRow><TableCell colSpan={8} className="py-8 text-center text-muted-foreground">No problems match these filters.</TableCell></TableRow>
          )}
        </TableBody>
      </Table>

      <section>
        <h2 className="mb-1 text-sm font-medium">Progress by topic</h2>
        <Chart option={chartOption} height={240} />
      </section>
    </div>
  )
}
