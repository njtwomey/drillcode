import { Fragment, type ReactNode } from 'react'

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
export function Description({ source }: { source: string }) {
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
    </div>
  )
}
