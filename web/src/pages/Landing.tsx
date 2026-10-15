import { ArrowDown, ArrowUp, ArrowUpDown, Check, Dices, ExternalLink, Search, X } from 'lucide-react'
import { useMemo } from 'react'
import { Link, useNavigate } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
import { MultiSelect } from '@/components/MultiSelect'
import { StatusToggle } from '@/components/StatusToggle'
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

/** A topic or tag that filters the list when clicked. */
function TopicLink({ topic, primary }: { topic: string; primary?: boolean }) {
  const setFilters = useStore((s) => s.setFilters)
  return (
    <button onClick={() => setFilters({ topics: [topic] })} title={`Show only ${topic} problems`}>
      <Badge variant={primary ? 'secondary' : 'outline'} className="cursor-pointer hover:bg-accent hover:text-accent-foreground">
        {topic}
      </Badge>
    </button>
  )
}

export function Landing() {
  const navigate = useNavigate()
  const done = useStore((s) => s.done)
  const filters = useStore((s) => s.filters)
  const sort = useStore((s) => s.sort)
  const { toggleDone, setFilters, clearFilters, setSort } = useStore()

  const filtered = useMemo(() => {
    const rows = problems.filter((p) => matchesFilter(p, filters, done))
    if (!sort.key) return rows
    const sorted = [...rows].sort(compare(sort.key, done))
    return sort.dir === 'desc' ? sorted.reverse() : sorted
  }, [filters, done, sort])

  const doneInView = filtered.filter((p) => done[p.slug]).length
  const filtering =
    filters.search || filters.difficulties.length || filters.topics.length || filters.blind75Only || filters.status !== 'all'

  function clickHeader(key: SortKey) {
    if (sort.key !== key) setSort({ key, dir: 'asc' })
    else if (sort.dir === 'asc') setSort({ key, dir: 'desc' })
    else setSort({ key: null, dir: 'asc' })
  }

  function randomProblem() {
    const pick = filtered[Math.floor(Math.random() * filtered.length)]
    if (pick) navigate(`/p/${pick.slug}`)
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
          <div className="flex items-center gap-2">
            <span className="text-muted-foreground">Show</span>
            <StatusToggle value={filters.status} onChange={(status) => setFilters({ status })} />
          </div>
          <Label className="gap-2 font-normal">
            <Switch checked={filters.blind75Only} onCheckedChange={(c) => setFilters({ blind75Only: c })} />
            Only the Blind 75
          </Label>
          {filtering ? (
            <Button variant="ghost" size="sm" onClick={clearFilters}><X /> Clear filters</Button>
          ) : null}
          <span className="ml-auto text-muted-foreground">
            Showing {filtered.length} of {problems.length} · {doneInView} done
          </span>
          <Button size="sm" variant="outline" onClick={randomProblem} disabled={!filtered.length} title="Open a random problem from the ones shown">
            <Dices /> Random problem
          </Button>
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
              <TableCell><TopicLink topic={p.topic} primary /></TableCell>
              <TableCell className="space-x-1">{p.tags.map((t) => <TopicLink key={t} topic={t} />)}</TableCell>
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
    </div>
  )
}
