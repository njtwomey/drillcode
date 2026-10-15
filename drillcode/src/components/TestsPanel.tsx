import { ChevronDown, ChevronRight, Play, Terminal } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { StatusBadge } from '@/components/badges'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { formatCase } from '@/lib/caseFormat'
import type { CaseResult, TestCase, TestsSpec } from '@/lib/types'

interface Props {
  spec: TestsSpec
  cases: TestCase[]
  results: Record<string, CaseResult | undefined>
  selected: Set<string>
  running: boolean
  onToggle: (name: string) => void
  onSelectAll: () => void
  onSelectNone: () => void
  onRunOne: (name: string) => void
  /** Practice mode: only the first `hideAfter` catalogue cases are shown by name and input; the rest are hidden until they fail. */
  hideAfter?: number
}

const show = (v: unknown) => JSON.stringify(v)
const hasOutput = (r?: CaseResult) => !!r && !!(r.stdout.trim() || r.stderr.trim())

/** Every test case: tick the ones to run, open one to see its input, result and console output, or run it alone. */
export function TestsPanel({ spec, cases, results, selected, running, onToggle, onSelectAll, onSelectNone, onRunOne, hideAfter }: Props) {
  const [open, setOpen] = useState<Record<string, boolean>>({})
  // Failures open themselves once per run, so the reason is on screen; the reader can still close them.
  const autoOpened = useRef(new Set<string>())
  useEffect(() => {
    const opened: Record<string, boolean> = {}
    for (const c of cases) {
      const r = results[c.name]
      const bad = !!r && r.status !== 'pass' && r.status !== 'skipped'
      if (bad && !autoOpened.current.has(c.name)) {
        autoOpened.current.add(c.name)
        opened[c.name] = true
      }
      if (!bad) autoOpened.current.delete(c.name)
    }
    if (Object.keys(opened).length) setOpen((o) => ({ ...o, ...opened }))
  }, [results, cases])

  const allOpen = cases.every((c) => open[c.name])
  const setAll = (value: boolean) => setOpen(Object.fromEntries(cases.map((c) => [c.name, value])))

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-1.5 text-xs">
        <Button size="sm" variant="ghost" className="h-7 px-2" onClick={onSelectAll}>Select all</Button>
        <Button size="sm" variant="ghost" className="h-7 px-2" onClick={onSelectNone}>Select none</Button>
        <Button size="sm" variant="ghost" className="ml-auto h-7 px-2" onClick={() => setAll(!allOpen)}>
          {allOpen ? 'Collapse all' : 'Expand all'}
        </Button>
      </div>
      <ul className="divide-y rounded-md border text-sm">
        {cases.map((c, i) => {
          const r = results[c.name]
          const hidden = hideAfter !== undefined && !c.custom && i >= hideAfter
          const failed = !!r && r.status !== 'pass' && r.status !== 'skipped'
          const isOpen = !!open[c.name]
          const label = hidden ? `Hidden case ${i - hideAfter + 1}` : c.name
          return (
            <li key={c.name}>
              <Collapsible open={isOpen} onOpenChange={(v) => setOpen((o) => ({ ...o, [c.name]: v }))}>
                <div className="flex items-center gap-1.5 px-2 py-1.5">
                  <Checkbox checked={selected.has(c.name)} onCheckedChange={() => onToggle(c.name)} aria-label={`Run ${label}`} />
                  <CollapsibleTrigger asChild>
                    <button className="flex min-w-0 flex-1 items-center gap-1.5 text-left" aria-label={`${isOpen ? 'Collapse' : 'Expand'} ${label}`}>
                      {isOpen ? <ChevronDown className="size-4 shrink-0 text-muted-foreground" /> : <ChevronRight className="size-4 shrink-0 text-muted-foreground" />}
                      {r ? <StatusBadge status={r.status} /> : <Badge variant="outline" className="text-muted-foreground">not run</Badge>}
                      <span className="min-w-0 truncate font-medium">{label}</span>
                      {c.custom && <Badge variant="outline">custom</Badge>}
                      {hasOutput(r) && <Terminal className="size-3.5 shrink-0 text-muted-foreground" aria-label="Has console output" />}
                      {r && r.status !== 'skipped' && <span className="ml-auto shrink-0 text-xs text-muted-foreground tabular-nums">{r.ms.toFixed(2)} ms</span>}
                    </button>
                  </CollapsibleTrigger>
                  <Button size="icon" variant="ghost" className="size-7 shrink-0" disabled={running} onClick={() => onRunOne(c.name)} aria-label={`Run only ${label}`} title="Run only this test">
                    <Play className="size-3.5" />
                  </Button>
                </div>
                <CollapsibleContent>
                  <div className="space-y-2 border-t bg-muted/20 px-3 py-2">
                    {(!hidden || failed) && (
                      <div className="break-all font-mono text-xs text-muted-foreground">
                        {hidden ? formatCase(spec, { ...c, expected: undefined }).replace(/ → undefined$/, '') : formatCase(spec, c)}
                      </div>
                    )}
                    {r?.status === 'fail' && (
                      <div className="grid gap-2 rounded-md bg-muted/50 p-2 font-mono text-xs sm:grid-cols-2">
                        <div className="break-all"><span className="text-muted-foreground">expected </span>{show(r.expected)}</div>
                        <div className="break-all"><span className="text-muted-foreground">got </span>{show(r.actual)}</div>
                        {r.message && r.message !== 'Output does not match expected' && (
                          <div className="break-all text-muted-foreground sm:col-span-2">{r.message}</div>
                        )}
                      </div>
                    )}
                    {r && (r.status === 'error' || r.status === 'timeout') && r.message && (
                      <pre className="max-h-48 overflow-auto rounded-md bg-muted/50 p-2 text-xs whitespace-pre-wrap">{r.message}</pre>
                    )}
                    {!r && <p className="text-xs text-muted-foreground">Not run yet.</p>}
                    {r?.status === 'pass' && !hasOutput(r) && <p className="text-xs text-muted-foreground">Passed. Nothing was printed.</p>}
                    {hasOutput(r) && (
                      <Collapsible>
                        <CollapsibleTrigger className="flex items-center gap-1 text-xs font-medium text-muted-foreground hover:text-foreground">
                          <Terminal className="size-3.5" /> Console output
                        </CollapsibleTrigger>
                        <CollapsibleContent>
                          <pre className="mt-1 max-h-48 overflow-auto rounded-md border bg-background p-2 font-mono text-xs whitespace-pre-wrap">
                            {[r!.stdout, r!.stderr].filter((t) => t.trim()).join('\n').trimEnd()}
                          </pre>
                        </CollapsibleContent>
                      </Collapsible>
                    )}
                  </div>
                </CollapsibleContent>
              </Collapsible>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
