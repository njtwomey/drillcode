import { ExternalLink } from 'lucide-react'
import { Description } from '@/components/Description'
import { Workspace } from '@/components/Workspace'
import { bySlug, definitions, descriptionSource, skeletonSource } from '@/lib/catalogue'
import { practiceDraftKey } from '@/lib/store'
import type { CaseResult } from '@/lib/types'

/** In practice only the first two catalogue cases are shown; the rest are hidden cases that just report pass or fail. */
const VISIBLE_EXAMPLES = 2

/** One problem in practice mode: description and judge notes only (no approach, no hints), a blank skeleton, hidden tests. */
export function PracticeProblem({ slug, onResults }: { slug: string; onResults: (results: CaseResult[]) => void }) {
  const problem = bySlug.get(slug)!
  const defs = definitions(slug)
  const description = descriptionSource(slug)
  return (
    <Workspace
      key={slug}
      slug={slug}
      visibleExamples={VISIBLE_EXAMPLES}
      draftKey={practiceDraftKey(slug)}
      originalSource={skeletonSource(slug)}
      onResults={onResults}
      left={
        <aside className="space-y-4 text-sm">
          {description && <Description source={description} slug={slug} />}
          <a href={problem.leetcode} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 underline">
            Full statement on LeetCode <ExternalLink className="size-3" />
          </a>
          <p className="rounded-md border p-3 text-muted-foreground">
            Practice mode: no solution, approach or hints. The first two test cases are shown as examples; the rest
            are hidden cases that only report whether they passed.
          </p>
          {defs && (
            <div className="rounded-md border p-3">
              <h2 className="mb-2 font-medium">Definitions and judge notes</h2>
              <pre className="overflow-auto font-mono text-xs">{defs}</pre>
            </div>
          )}
        </aside>
      }
    />
  )
}
