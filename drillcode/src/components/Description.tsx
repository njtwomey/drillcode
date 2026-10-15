import { Fragment, type ReactNode } from 'react'
import { testsSpec } from '@/lib/catalogue'
import { formatNamedCase } from '@/lib/caseFormat'

/** Inline `code` spans. */
function inline(text: string): ReactNode[] {
  return text.split(/(`[^`]+`)/g).map((part, i) =>
    part.startsWith('`') && part.endsWith('`') && part.length > 2 ? (
      <code key={i} className="rounded bg-muted px-1 py-0.5 font-mono text-[0.85em]">{part.slice(1, -1)}</code>
    ) : (
      <Fragment key={i}>{part}</Fragment>
    ),
  )
}

/** The tiny markdown subset descriptions use: paragraphs, "- " bullets, `code`. */
export function Description({ source, slug }: { source: string; slug?: string }) {
  const blocks = source.trim().split(/\n\s*\n/)
  return (
    <div className="space-y-2 text-sm leading-relaxed">
      {blocks.map((block, i) => {
        const lines = block.split('\n')
        const bullets = lines.filter((l) => l.startsWith('- '))
        const lead = lines.filter((l) => !l.startsWith('- ')).join(' ')
        return (
          <Fragment key={i}>
            {lead && <p>{inline(lead)}</p>}
            {bullets.length > 0 && (
              <ul className="list-disc space-y-1 pl-5">
                {bullets.map((b, j) => <li key={j}>{inline(b.slice(2))}</li>)}
              </ul>
            )}
          </Fragment>
        )
      })}
      {slug && <Examples slug={slug} />}
    </div>
  )
}

/** The first two catalogue cases (the public examples), as a list in the style of the constraints. Only shown when they have an answer. */
function Examples({ slug }: { slug: string }) {
  const spec = testsSpec(slug)
  // Where the harness checks behaviour itself (`call: false`) the expected value is a bare pass flag, which says nothing.
  if (!spec || spec.call === false) return null
  const shown = spec.cases.slice(0, 2).filter((c) => c.expected !== undefined)
  if (shown.length === 0) return null
  return (
    <>
      <p>Examples:</p>
      <ul className="list-disc space-y-1 pl-5">
        {shown.map((c) => (
          <li key={c.name}><code className="break-words rounded bg-muted px-1 py-0.5 font-mono text-[0.85em]">{formatNamedCase(spec, c)}</code></li>
        ))}
      </ul>
    </>
  )
}
