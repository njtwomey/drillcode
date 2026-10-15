import { Search, X } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link } from 'react-router'
import { ChipButton, ChipLink } from '@/components/ChipLink'
import { MultiSelect } from '@/components/MultiSelect'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { bySlug, TOPICS } from '@/lib/catalogue'
import { AREAS, searchText, signalRows, techniqueBySlug, techniques, type Technique } from '@/lib/techniques'

const SORTED_AREAS = [...AREAS].sort((a, b) => a.localeCompare(b))

/** "I'm stuck, what should I try?": search everything, jump from a signal to a technique, or browse by area. */
export function Tips() {
  const [search, setSearch] = useState('')
  const [areas, setAreas] = useState<string[]>([])
  const [topics, setTopics] = useState<string[]>([])

  const index = useMemo(() => new Map(techniques.map((t) => [t.slug, searchText(t)])), [])
  const words = search.toLowerCase().split(/\s+/).filter(Boolean)

  const matches = (t: Technique) =>
    (!areas.length || areas.includes(t.area)) &&
    (!topics.length || topics.some((x) => t.topics.includes(x))) &&
    words.every((w) => index.get(t.slug)!.includes(w))

  const shown = techniques.filter(matches)
  const shownSlugs = new Set(shown.map((t) => t.slug))
  // A signal card stays if one of its techniques matches, or the search words appear in the signal text itself.
  const signals = signalRows.filter(
    (r) =>
      r.slugs.some((s) => shownSlugs.has(s)) ||
      (!areas.length && !topics.length && words.length > 0 && words.every((w) => r.signal.toLowerCase().includes(w))),
  )
  const filtering = search || areas.length || topics.length
  const groups = AREAS.map((area) => ({ area, items: shown.filter((t) => t.area === area) })).filter((g) => g.items.length)

  function clear() {
    setSearch('')
    setAreas([])
    setTopics([])
  }

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <div className="space-y-4">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold">Tips</h1>
          <p className="text-sm text-muted-foreground">
            Stuck on a problem? Search for what it says or what you see, or start from a signal below.
          </p>
        </div>
        <div className="relative">
          <Search className="absolute top-3 left-3.5 size-5 text-muted-foreground" />
          <Input
            autoFocus
            className="h-11 pr-10 pl-11 text-base"
            placeholder="Search everything: a signal, a technique, a topic, a problem (e.g. “head may change”, “window”, “lru”)"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          {search && (
            <button className="absolute top-3 right-3 text-muted-foreground hover:text-foreground" aria-label="Clear search" onClick={() => setSearch('')}>
              <X className="size-5" />
            </button>
          )}
        </div>
        <div className="flex flex-wrap items-end gap-3">
          <div className="w-56"><MultiSelect label="Area" allLabel="Any area" options={SORTED_AREAS} value={areas} onChange={setAreas} /></div>
          <div className="w-56"><MultiSelect label="Problem topic" allLabel="Any topic" options={TOPICS} value={topics} onChange={setTopics} columns={2} /></div>
          {filtering ? <Button variant="ghost" size="sm" onClick={clear}><X /> Clear</Button> : null}
          <span className="ml-auto text-sm text-muted-foreground">{shown.length} of {techniques.length} techniques</span>
        </div>
      </div>

      {signals.length > 0 && (
        <section className="space-y-3">
          <h2 className="text-sm font-semibold text-muted-foreground">When the problem says…</h2>
          <ul className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
            {signals.map((row) => (
              <li key={row.signal} className="flex flex-col justify-between gap-3 rounded-xl border bg-card p-4 shadow-xs">
                <p className="font-medium leading-snug">{row.signal}</p>
                <div className="flex flex-wrap items-center gap-1.5">
                  {row.parts.map((part, i) =>
                    'slug' in part ? (
                      techniqueBySlug.has(part.slug) ? (
                        <ChipLink key={i} to={`/tips/${part.slug}`}>{techniqueBySlug.get(part.slug)!.title}</ChipLink>
                      ) : null
                    ) : (
                      <span key={i} className="text-xs text-muted-foreground">{part.text.replace(/^[\s;,]+|[\s;,]+$/g, '')}</span>
                    ),
                  )}
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section className="space-y-6">
        {groups.length === 0 && <p className="text-sm text-muted-foreground">Nothing matches. Try fewer words, or clear the filters.</p>}
        {groups.map(({ area, items }) => (
          <div key={area} className="space-y-3">
            <h2 className="text-sm font-semibold text-muted-foreground">{area}</h2>
            <ul className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
              {items.map((t) => (
                <li key={t.slug} className="relative flex flex-col gap-3 rounded-xl border bg-card p-4 shadow-xs transition-colors hover:bg-muted/40">
                  <div className="space-y-1">
                    <Link to={`/tips/${t.slug}`} className="text-base font-semibold after:absolute after:inset-0 hover:underline">
                      {t.title}
                    </Link>
                    <p className="text-sm text-muted-foreground">{t.signal.replace(/`/g, '')}</p>
                  </div>
                  <div className="relative z-10 flex flex-wrap gap-1.5">
                    <ChipButton onClick={() => { setAreas([t.area]); setTopics([]) }} title={`Show only ${t.area}`}>{t.area}</ChipButton>
                    {t.topics.map((x) => (
                      <ChipButton key={x} onClick={() => { setTopics([x]); setAreas([]) }} title={`Show only ${x} techniques`}>{x}</ChipButton>
                    ))}
                  </div>
                  <div className="relative z-10 mt-auto flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
                    <span>Used in</span>
                    {t.problems.slice(0, 3).map((slug) => (
                      <Link key={slug} to={`/p/${slug}`} className="rounded-md bg-muted px-1.5 py-0.5 hover:underline">
                        {bySlug.get(slug)?.title ?? slug}
                      </Link>
                    ))}
                    {t.problems.length > 3 && <Badge variant="outline">+{t.problems.length - 3} more</Badge>}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>
    </div>
  )
}
