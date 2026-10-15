import { Fragment, type ReactNode, useMemo } from 'react'
import { testsSpec } from '@/lib/catalogue'
import { EXAMPLES_SHOWN, formatNamedCase } from '@/lib/caseFormat'

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

const MAX_EXAMPLE = 160

/** The statement's examples: of the first two catalogue cases (the ones Practice shows), those named "example ...". */
function Examples({ slug }: { slug: string }) {
  const spec = useMemo(() => testsSpec(slug), [slug])
  // Where the harness checks behaviour itself (`call: false`) the expected value is a bare pass flag, which says nothing.
  if (!spec || spec.call === false) return null
  const shown = spec.cases.slice(0, EXAMPLES_SHOWN).filter((c) => c.name.startsWith('example') && c.expected !== undefined)
  if (shown.length === 0) return null
  return (
    <>
      <p>Examples{spec.compare === 'validator' ? ' (any valid answer is accepted)' : ''}:</p>
      <ul className="list-disc space-y-1 pl-5">
        {shown.map((c) => {
          const line = formatNamedCase(spec, c)
          return (
            <li key={c.name}>
              <code title={line.length > MAX_EXAMPLE ? line : undefined} className="break-words rounded bg-muted px-1 py-0.5 font-mono text-[0.85em]">
                {line.length > MAX_EXAMPLE ? `${line.slice(0, MAX_EXAMPLE)}…` : line}
              </code>
            </li>
          )
        })}
      </ul>
    </>
  )
}
