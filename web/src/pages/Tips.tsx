import { Search, X } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link } from 'react-router'
import { Markdown } from '@/components/Markdown'
import { MultiSelect } from '@/components/MultiSelect'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { TOPICS } from '@/lib/catalogue'
import { AREAS, signalsTable, techniques } from '@/lib/techniques'

/** "I'm stuck, what should I try?": a signals table, then every technique, filterable by area and topic. */
export function Tips() {
  const [search, setSearch] = useState('')
  const [areas, setAreas] = useState<string[]>([])
  const [topics, setTopics] = useState<string[]>([])

  const shown = useMemo(() => {
    const words = search.toLowerCase().split(/\s+/).filter(Boolean)
    return techniques.filter((t) => {
      if (areas.length && !areas.includes(t.area)) return false
      if (topics.length && !topics.some((x) => t.topics.includes(x))) return false
      const haystack = `${t.title} ${t.area} ${t.topics.join(' ')} ${t.body}`.toLowerCase()
      return words.every((w) => haystack.includes(w))
    })
  }, [search, areas, topics])

  const filtering = search || areas.length || topics.length
  const groups = AREAS.map((area) => ({ area, items: shown.filter((t) => t.area === area) })).filter((g) => g.items.length)

  return (
    <div className="mx-auto max-w-5xl space-y-6">
      <div className="space-y-1">
        <h1 className="text-xl font-semibold">Tips</h1>
        <p className="text-sm text-muted-foreground">
          Tricks and templates for when a problem looks awkward. Every page links to the catalogue problems that use it.
        </p>
      </div>

      <section className="space-y-2">
        <h2 className="text-sm font-medium">Which technique?</h2>
        <Markdown source={signalsTable} />
      </section>

      <section className="space-y-4">
        <h2 className="text-sm font-medium">All techniques</h2>
        <div className="grid items-end gap-3 rounded-lg border p-4 md:grid-cols-[minmax(200px,1fr)_220px_220px_auto]">
          <div className="space-y-1">
            <Label htmlFor="tips-search" className="text-xs text-muted-foreground">Search</Label>
            <div className="relative">
              <Search className="absolute top-2 left-2.5 size-4 text-muted-foreground" />
              <Input id="tips-search" className="h-8 pl-8" placeholder="e.g. dummy, window, cycle" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
          </div>
          <MultiSelect label="Area" allLabel="Any area" options={AREAS} value={areas as (typeof AREAS)[number][]} onChange={setAreas} />
          <MultiSelect label="Problem topic" allLabel="Any topic" options={TOPICS} value={topics} onChange={setTopics} columns={2} />
          {filtering ? (
            <Button variant="ghost" size="sm" onClick={() => { setSearch(''); setAreas([]); setTopics([]) }}><X /> Clear</Button>
          ) : <span />}
        </div>

        {groups.length === 0 && <p className="text-sm text-muted-foreground">No technique matches these filters.</p>}
        {groups.map(({ area, items }) => (
          <div key={area} className="space-y-2">
            <h3 className="text-sm font-semibold text-muted-foreground">{area}</h3>
            <ul className="grid gap-2 md:grid-cols-2">
              {items.map((t) => (
                <li key={t.slug}>
                  <Link to={`/tips/${t.slug}`} className="block h-full rounded-lg border p-3 hover:bg-muted/50">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-medium">{t.title}</span>
                      <Badge variant="secondary">{t.problems.length} problem{t.problems.length === 1 ? '' : 's'}</Badge>
                    </div>
                    <p className="mt-1 text-sm text-muted-foreground">{t.signal.replace(/`/g, '')}</p>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    </div>
  )
}
