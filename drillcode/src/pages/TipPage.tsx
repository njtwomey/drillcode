import { Check } from 'lucide-react'
import { Link, useParams } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
import { Markdown } from '@/components/Markdown'
import { Badge } from '@/components/ui/badge'
import { bySlug } from '@/lib/catalogue'
import { useStore } from '@/lib/store'
import { techniqueBySlug } from '@/lib/techniques'

export function TipPage() {
  const { slug = '' } = useParams()
  const done = useStore((s) => s.done)
  const tip = techniqueBySlug.get(slug)
  if (!tip) {
    return <p className="text-sm">Unknown tip “{slug}”. <Link className="underline" to="/tips">Back to all tips</Link></p>
  }
  return (
    <article className="mx-auto max-w-3xl space-y-6">
      <div className="space-y-2">
        <Link to="/tips" className="text-xs text-muted-foreground hover:underline">← All tips</Link>
        <h1 className="text-2xl font-semibold">{tip.title}</h1>
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="secondary">{tip.area}</Badge>
          {tip.topics.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}
        </div>
      </div>

      {tip.sections.map((s) => (
        <section key={s.heading} className="space-y-2">
          <h2 className="text-base font-semibold">{s.heading}</h2>
          <Markdown source={s.body} copyCode={s.heading === 'Template'} />
        </section>
      ))}

      <section className="space-y-2">
        <h2 className="text-base font-semibold">Problems in the catalogue</h2>
        <ul className="divide-y rounded-md border text-sm">
          {tip.problems.map((p) => {
            const problem = bySlug.get(p)
            if (!problem) return null
            return (
              <li key={p}>
                <Link to={`/p/${p}/view`} className="flex items-center gap-3 px-3 py-2 hover:bg-muted/50">
                  <span className="w-10 text-muted-foreground tabular-nums">{problem.number}</span>
                  <span className="flex-1 font-medium">{problem.title}</span>
                  <DifficultyBadge difficulty={problem.difficulty} />
                  {done[p] ? <Check className="size-4 text-green-600" aria-label="Done" /> : <span className="size-4" />}
                </Link>
              </li>
            )
          })}
        </ul>
      </section>

      {tip.related.length > 0 && (
        <section className="space-y-2">
          <h2 className="text-base font-semibold">Related techniques</h2>
          <div className="flex flex-wrap gap-2">
            {tip.related.map((r) => (
              <Link key={r} to={`/tips/${r}`}><Badge variant="outline" className="hover:bg-muted">{techniqueBySlug.get(r)?.title ?? r}</Badge></Link>
            ))}
          </div>
        </section>
      )}
    </article>
  )
}
