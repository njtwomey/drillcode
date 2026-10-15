import { Badge } from '@/components/ui/badge'
import { StatusBadge } from '@/components/badges'
import { formatCase } from '@/lib/caseFormat'
import type { CaseResult, TestCase, TestsSpec } from '@/lib/types'

interface Props {
  spec: TestsSpec
  cases: TestCase[]
  results: CaseResult[]
  /** Practice mode: only the first `examples` catalogue cases are shown; the rest are hidden until they fail. */
  hideAfter?: number
}

const show = (v: unknown) => JSON.stringify(v)

/** Every test case, as one readable line each, with its result once the tests have run. */
export function TestsPanel({ spec, cases, results, hideAfter }: Props) {
  const catalogueCount = spec.cases.length
  return (
    <ul className="divide-y rounded-md border text-sm">
      {cases.map((c, i) => {
        const result = results[i]
        const hidden = hideAfter !== undefined && !c.custom && i >= hideAfter
        const failed = result && result.status !== 'pass' && result.status !== 'skipped'
        return (
          <li key={`${c.name}-${i}`} className="px-3 py-2">
            <div className="flex items-start gap-3">
              <div className="w-20 shrink-0 pt-0.5">
                {result ? <StatusBadge status={result.status} /> : <Badge variant="outline" className="text-muted-foreground">not run</Badge>}
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-medium">{hidden ? `Hidden case ${i - hideAfter + 1}` : c.name}</span>
                  {c.custom && <Badge variant="outline">custom</Badge>}
                  {i >= catalogueCount && !c.custom && null}
                  {result && result.status !== 'skipped' && (
                    <span className="text-xs text-muted-foreground tabular-nums">{result.ms.toFixed(2)} ms</span>
                  )}
                </div>
                {!hidden && <div className="mt-0.5 break-all font-mono text-xs text-muted-foreground">{formatCase(spec, c)}</div>}
                {failed && result.status === 'fail' && (
                  <div className="mt-2 grid gap-2 rounded-md bg-muted/50 p-2 font-mono text-xs sm:grid-cols-2">
                    {hidden && <div className="break-all sm:col-span-2"><span className="text-muted-foreground">input </span>{formatCase(spec, { ...c, expected: undefined }).replace(/ → undefined$/, '')}</div>}
                    <div className="break-all"><span className="text-muted-foreground">expected </span>{show(result.expected)}</div>
                    <div className="break-all"><span className="text-muted-foreground">got </span>{show(result.actual)}</div>
                    {result.message && result.message !== 'Output does not match expected' && (
                      <div className="break-all text-muted-foreground sm:col-span-2">{result.message}</div>
                    )}
                  </div>
                )}
                {failed && result.status !== 'fail' && result.message && (
                  <pre className="mt-2 max-h-40 overflow-auto rounded-md bg-muted/50 p-2 text-xs whitespace-pre-wrap">{result.message}</pre>
                )}
              </div>
            </div>
          </li>
        )
      })}
    </ul>
  )
}
