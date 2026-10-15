import { ChevronDown, ChevronRight, ChevronsDownUp, ChevronsUpDown, Lock, Pencil, Play, Terminal, Trash2 } from 'lucide-react'
import { useEffect, useRef, useState, type ReactNode } from 'react'
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
  onSelectMine: () => void
  onRunOne: (name: string) => void
  /** The case being edited (its row opens with the editor in it), and how to start, finish and delete. */
  editing?: string | null
  onEdit?: (name: string | null) => void
  onDelete?: (name: string) => void
  renderEditor?: (c: TestCase) => ReactNode
  /** Exposure: only the first `visibleExamples` catalogue cases are shown by name and input; the rest are hidden cases that cannot be opened. Undefined shows everything. */
  visibleExamples?: number
}

const show = (v: unknown) => JSON.stringify(v)
/** A hidden case: a catalogue case past the first `visibleExamples`. It shows a status only and cannot be opened. */
function isHiddenCase(spec: TestsSpec, visibleExamples: number | undefined, c: TestCase): boolean {
  return visibleExamples !== undefined && !c.custom && spec.cases.findIndex((x) => x.name === c.name) >= visibleExamples
}

const hasOutput = (r?: CaseResult) => !!r && !!(r.stdout.trim() || r.stderr.trim())

/** Every test case: tick the ones to run, open one to see its input, result and console output, or run it alone. */
export function TestsPanel({ spec, cases, results, selected, running, onToggle, onSelectAll, onSelectNone, onSelectMine, onRunOne, editing, onEdit, onDelete, renderEditor, visibleExamples }: Props) {
  const [open, setOpen] = useState<Record<string, boolean>>({})
  // Failures open themselves once per run, so the reason is on screen; the reader can still close them.
  const autoOpened = useRef(new Set<string>())
  useEffect(() => {
    const opened: Record<string, boolean> = {}
    for (const c of cases) {
      const r = results[c.name]
      const bad = !!r && r.status !== 'pass' && r.status !== 'skipped' && !isHiddenCase(spec, visibleExamples, c)
      if (bad && !autoOpened.current.has(c.name)) {
        autoOpened.current.add(c.name)
        opened[c.name] = true
      }
      if (!bad) autoOpened.current.delete(c.name)
    }
    if (Object.keys(opened).length) setOpen((o) => ({ ...o, ...opened }))
  }, [results, cases, spec, visibleExamples])

  const openable = cases.filter((c) => !isHiddenCase(spec, visibleExamples, c))
  const setAll = (value: boolean) => setOpen(Object.fromEntries(openable.map((c) => [c.name, value])))
  const hasMine = cases.some((c) => c.custom)

  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-1.5 text-xs">
        <Button size="sm" variant="ghost" className="h-7 px-2" onClick={onSelectAll}>Select all</Button>
        <Button size="sm" variant="ghost" className="h-7 px-2" onClick={onSelectNone}>Select none</Button>
        <Button size="sm" variant="ghost" className="h-7 px-2" onClick={onSelectMine} disabled={!hasMine} title="Select only the test cases you added">
          Select mine
        </Button>
        <div className="ml-auto flex items-center">
          <Button size="icon" variant="ghost" className="size-7" onClick={() => setAll(true)} disabled={openable.length === 0} aria-label="Expand all" title="Expand all">
            <ChevronsUpDown className="size-4" />
          </Button>
          <Button size="icon" variant="ghost" className="size-7" onClick={() => setAll(false)} disabled={openable.length === 0} aria-label="Collapse all" title="Collapse all">
            <ChevronsDownUp className="size-4" />
          </Button>
        </div>
      </div>
      <ul className="divide-y rounded-md border text-sm">
        {cases.map((c) => {
          const r = results[c.name]
          const hidden = isHiddenCase(spec, visibleExamples, c)
          const failed = !!r && r.status !== 'pass' && r.status !== 'skipped'
          const isEditing = editing === c.name
          const isOpen = !hidden && (isEditing || !!open[c.name])
          const label = hidden ? `Hidden case ${spec.cases.findIndex((x) => x.name === c.name) - visibleExamples! + 1}` : c.name
          if (hidden) {
            return (
              <li key={c.name} className="flex items-center gap-1.5 px-2 py-1.5">
                <Checkbox checked={selected.has(c.name)} onCheckedChange={() => onToggle(c.name)} aria-label={`Run ${label}`} />
                <Lock className="size-4 shrink-0 text-muted-foreground" aria-hidden />
                {r ? <StatusBadge status={r.status} /> : <Badge variant="outline" className="text-muted-foreground">not run</Badge>}
                <span className="min-w-0 truncate font-medium">{label}</span>
                {failed && <span className="truncate text-xs text-muted-foreground">did not pass; its input stays hidden</span>}
                {r && r.status !== 'skipped' && <span className="ml-auto shrink-0 text-xs text-muted-foreground tabular-nums">{r.ms.toFixed(2)} ms</span>}
                <Button size="icon" variant="ghost" className="size-7 shrink-0" disabled={running} onClick={() => onRunOne(c.name)} aria-label={`Run only ${label}`} title="Run only this test">
                  <Play className="size-3.5" />
                </Button>
              </li>
            )
          }
          return (
            <li key={c.name}>
              <Collapsible open={isOpen} onOpenChange={(v) => !isEditing && setOpen((o) => ({ ...o, [c.name]: v }))}>
                <div className="flex items-center gap-1.5 px-2 py-1.5">
                  <Checkbox checked={selected.has(c.name)} onCheckedChange={() => onToggle(c.name)} aria-label={`Run ${label}`} />
                  <CollapsibleTrigger asChild>
                    <button className="flex min-w-0 flex-1 items-center gap-1.5 text-left" aria-label={`${isOpen ? 'Collapse' : 'Expand'} ${label}`}>
                      {isOpen ? <ChevronDown className="size-4 shrink-0 text-muted-foreground" /> : <ChevronRight className="size-4 shrink-0 text-muted-foreground" />}
                      {r ? <StatusBadge status={r.status} /> : <Badge variant="outline" className="text-muted-foreground">not run</Badge>}
                      <span className="min-w-0 flex-1">
                        <span className="flex items-center gap-1.5">
                          <span className="min-w-0 truncate font-medium">{label}</span>
                          {c.custom && <Badge variant="outline">custom</Badge>}
                          {hasOutput(r) && <Terminal className="size-3.5 shrink-0 text-muted-foreground" aria-label="Has console output" />}
                        </span>
                        {c.custom && (
                          <span className="block truncate font-mono text-xs text-muted-foreground" title={formatCase(spec, c)}>
                            {formatCase(spec, c)}
                          </span>
                        )}
                      </span>
                      {r && r.status !== 'skipped' && <span className="shrink-0 text-xs text-muted-foreground tabular-nums">{r.ms.toFixed(2)} ms</span>}
                    </button>
                  </CollapsibleTrigger>
                  <Button size="icon" variant="ghost" className="size-7 shrink-0" disabled={running} onClick={() => onRunOne(c.name)} aria-label={`Run only ${label}`} title="Run only this test">
                    <Play className="size-3.5" />
                  </Button>
                  {c.custom && onEdit && (
                    <Button size="icon" variant="ghost" className="size-7 shrink-0" onClick={() => onEdit(isEditing ? null : c.name)} aria-label={`Edit ${label}`} title="Edit this case">
                      <Pencil className="size-3.5" />
                    </Button>
                  )}
                  {c.custom && onDelete && (
                    <Button size="icon" variant="ghost" className="size-7 shrink-0" onClick={() => onDelete(c.name)} aria-label={`Delete ${label}`} title="Delete this case">
                      <Trash2 className="size-3.5" />
                    </Button>
                  )}
                </div>
                <CollapsibleContent>
                  <div className="space-y-2 border-t bg-muted/20 px-3 py-2">
                    {isEditing && renderEditor ? renderEditor(c) : (<>
                    <div className="break-all font-mono text-xs text-muted-foreground">{formatCase(spec, c)}</div>
                    {r?.status === 'fail' && (
                      <div className="grid gap-1 rounded-md bg-muted/50 p-2 font-mono text-xs">
                        <div className="break-all">
                          <span className="text-muted-foreground">expected </span>{show(r.expected)}
                          {(c.derived || r.expected_source === 'reference') && <span className="ml-1 font-sans text-muted-foreground">(from the reference solution)</span>}
                        </div>
                        <div className="break-all"><span className="text-muted-foreground">got </span>{show(r.actual)}</div>
                        {r.message && r.message !== 'Output does not match expected' && (
                          <div className="break-all text-muted-foreground">{r.message}</div>
                        )}
                      </div>
                    )}
                    {r && (r.status === 'error' || r.status === 'timeout') && r.message && (
                      <pre className="max-h-48 overflow-auto rounded-md bg-muted/50 p-2 text-xs whitespace-pre-wrap">{r.message}</pre>
                    )}
                    {!r && <p className="text-xs text-muted-foreground">Not run yet.</p>}
                    {r?.status === 'pass' && (c.derived || r.expected_source === 'reference') && (
                      <p className="break-all text-xs text-muted-foreground">Matched the reference solution’s answer: <span className="font-mono">{show(r.expected)}</span></p>
                    )}
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
                    </>)}
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
