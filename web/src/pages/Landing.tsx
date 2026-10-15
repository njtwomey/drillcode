import { ExternalLink, Shuffle, Play, X, Check } from 'lucide-react'
import { useMemo } from 'react'
import { Link, useNavigate } from 'react-router'
import { Chart } from '@/components/Chart'
import { DifficultyBadge } from '@/components/badges'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { problems, TOPICS } from '@/lib/catalogue'
import { useStore } from '@/lib/store'
import type { Difficulty } from '@/lib/types'

export function Landing() {
  const navigate = useNavigate()
  const { done, filters, queue, toggleDone, setFilters, setQueue, clearQueue } = useStore()

  const filtered = useMemo(() => {
    const search = filters.search.trim().toLowerCase()
    return problems.filter((p) => {
      if (filters.difficulties.length && !filters.difficulties.includes(p.difficulty)) return false
      if (filters.topics.length && !filters.topics.some((t) => t === p.topic || p.tags.includes(t))) return false
      if (filters.blind75Only && !p.blind75) return false
      if (filters.hideDone && done[p.slug]) return false
      if (search && !(String(p.number) === search || p.title.toLowerCase().includes(search) || String(p.number).startsWith(search))) return false
      return true
    })
  }, [filters, done])

  // hideDone would otherwise make "n of m done" always read 0, so count over the non-done-filtered set.
  const scope = useMemo(
    () => (filters.hideDone ? problems.filter((p) => filtered.includes(p) || done[p.slug]) : filtered),
    [filters.hideDone, filtered, done],
  )
  const doneCount = scope.filter((p) => done[p.slug]).length

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
    <div className="space-y-4">
      <div className="grid gap-4 lg:grid-cols-[1fr_1.2fr]">
        <section className="space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <Input
              className="h-8 w-56"
              placeholder="Search number or title"
              value={filters.search}
              onChange={(e) => setFilters({ search: e.target.value })}
            />
            <ToggleGroup
              type="multiple"
              variant="outline"
              size="sm"
              value={filters.difficulties}
              onValueChange={(v) => setFilters({ difficulties: v as Difficulty[] })}
            >
              {(['easy', 'medium', 'hard'] as const).map((d) => (
                <ToggleGroupItem key={d} value={d} className="capitalize">{d}</ToggleGroupItem>
              ))}
            </ToggleGroup>
          </div>
          <ToggleGroup
            type="multiple"
            variant="outline"
            size="sm"
            className="flex-wrap justify-start"
            value={filters.topics}
            onValueChange={(v) => setFilters({ topics: v })}
          >
            {TOPICS.map((t) => (
              <ToggleGroupItem key={t} value={t} className="text-xs">{t}</ToggleGroupItem>
            ))}
          </ToggleGroup>
          <div className="flex flex-wrap items-center gap-4 text-sm">
            <Label className="gap-2">
              <Checkbox checked={filters.blind75Only} onCheckedChange={(c) => setFilters({ blind75Only: c === true })} />
              Blind 75 only
            </Label>
            <Label className="gap-2">
              <Checkbox checked={filters.hideDone} onCheckedChange={(c) => setFilters({ hideDone: c === true })} />
              Hide done
            </Label>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium">{doneCount} of {scope.length} done</span>
            <Button size="sm" variant="outline" onClick={shuffle} disabled={!filtered.length}>
              <Shuffle /> Shuffle
            </Button>
            {queue.length > 0 && (
              <>
                <Button size="sm" onClick={() => navigate(`/p/${queue[0]}`)}>
                  <Play /> Start ({queue.length})
                </Button>
                <Button size="icon" variant="ghost" aria-label="Clear queue" onClick={clearQueue}>
                  <X />
                </Button>
              </>
            )}
          </div>
        </section>
        <section>
          <Chart option={chartOption} height={230} />
        </section>
      </div>

      <Table className="text-sm">
        <TableHeader>
          <TableRow>
            <TableHead className="w-8">Done</TableHead>
            <TableHead className="w-12">#</TableHead>
            <TableHead>Title</TableHead>
            <TableHead>Difficulty</TableHead>
            <TableHead>Topic</TableHead>
            <TableHead>Tags</TableHead>
            <TableHead className="w-24">Flags</TableHead>
            <TableHead className="w-8" />
          </TableRow>
        </TableHeader>
        <TableBody>
          {filtered.map((p) => (
            <TableRow key={p.slug} className={done[p.slug] ? 'opacity-60' : ''}>
              <TableCell>
                <Checkbox checked={!!done[p.slug]} onCheckedChange={() => toggleDone(p.slug)} aria-label={`Mark ${p.title} done`} />
              </TableCell>
              <TableCell className="text-muted-foreground">{p.number}</TableCell>
              <TableCell>
                <Link to={`/p/${p.slug}`} className="font-medium hover:underline">{p.title}</Link>
              </TableCell>
              <TableCell><DifficultyBadge difficulty={p.difficulty} /></TableCell>
              <TableCell><Badge variant="secondary">{p.topic}</Badge></TableCell>
              <TableCell className="space-x-1">
                {p.tags.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}
              </TableCell>
              <TableCell className="space-x-1">
                {p.blind75 && <Badge variant="outline" title="Blind 75"><Check className="size-3" />75</Badge>}
                {p.premium && <Badge variant="outline" title="LeetCode premium">$</Badge>}
              </TableCell>
              <TableCell>
                <a href={p.leetcode} target="_blank" rel="noreferrer" aria-label="Open on LeetCode">
                  <ExternalLink className="size-4 text-muted-foreground hover:text-foreground" />
                </a>
              </TableCell>
            </TableRow>
          ))}
          {filtered.length === 0 && (
            <TableRow><TableCell colSpan={8} className="text-center text-muted-foreground">No problems match.</TableCell></TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  )
}
