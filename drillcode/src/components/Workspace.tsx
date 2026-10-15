import { ChevronDown, ChevronRight, PanelLeftClose, PanelLeftOpen, PanelRightClose, PanelRightOpen, Play, RotateCcw } from 'lucide-react'
import { useEffect, useRef, useState, useSyncExternalStore, type ReactNode } from 'react'
import { usePanelRef } from 'react-resizable-panels'
import { Benchmark } from '@/components/Benchmark'
import { CodeEditor } from '@/components/CodeEditor'
import { CustomCases } from '@/components/CustomCases'
import { TestsPanel } from '@/components/TestsPanel'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable'
import { testsSpec, validatorSource } from '@/lib/catalogue'
import { useStore } from '@/lib/store'
import type { CaseResult, TestCase } from '@/lib/types'
import { useIsWide } from '@/lib/useIsWide'
import { pyRunner } from '@/py/runner'

const NONE: TestCase[] = []
const STATUS_TEXT = {
  loading: 'Loading Python…',
  ready: 'Python ready',
  running: 'Running…',
  restarting: 'Restarting Python after a timeout…',
  error: 'Python failed to load',
} as const

interface Props {
  slug: string
  draftKey: string
  /** Editor text when there is no saved draft. */
  originalSource: string
  /** Content of the left column (description, notes). */
  left: ReactNode
  /** Extra toolbar controls (approach picker, walkthrough, Reveal). */
  toolbar?: ReactNode
  /** Practice: hide case names after the examples, no benchmark. */
  practice?: boolean
  /** Called only after a run that covered every test case. */
  onResults?: (results: CaseResult[]) => void
}

const EXAMPLES_SHOWN = 2

/**
 * Three columns: notes | code | tests. The side columns collapse and drag. Each test can be ticked,
 * run alone, opened, and carries its own console output; Run runs whatever is ticked.
 */
export function Workspace({ slug, draftKey, originalSource, left, toolbar, practice, onResults }: Props) {
  const spec = testsSpec(slug)!
  const drafts = useStore((s) => s.drafts)
  const theme = useStore((s) => s.theme)
  const custom = useStore((s) => s.customCases[slug]) ?? NONE
  const { setDraft, clearDraft } = useStore()
  const status = useSyncExternalStore(pyRunner.subscribe, pyRunner.getSnapshot)
  const wide = useIsWide()

  const [results, setResults] = useState<Record<string, CaseResult | undefined>>({})
  const [selected, setSelected] = useState<Set<string>>(() => new Set(spec.cases.map((c) => c.name)))
  const leftPanel = usePanelRef()
  const rightPanel = usePanelRef()
  const [leftCollapsed, setLeftCollapsed] = useState(false)
  const [rightCollapsed, setRightCollapsed] = useState(false)

  const source = drafts[draftKey] ?? originalSource
  const cases = [...spec.cases, ...custom.map((c) => ({ ...c, custom: true }))]
  const busy = status === 'running' || status === 'error'

  // A newly added custom case starts ticked.
  const known = useRef(new Set(spec.cases.map((c) => c.name)))
  useEffect(() => {
    const fresh = cases.filter((c) => !known.current.has(c.name))
    if (!fresh.length) return
    fresh.forEach((c) => known.current.add(c.name))
    setSelected((s) => new Set([...s, ...fresh.map((c) => c.name)]))
  })

  // CodeEditor keeps its onRun callback current, so these closures always see the latest text.
  async function runNames(names: string[]) {
    const subset = cases.filter((c) => names.includes(c.name))
    if (!subset.length || busy) return null
    setResults((prev) => {
      const next = { ...prev }
      subset.forEach((c) => delete next[c.name])
      return next
    })
    const job = { solutionSource: source, validatorSource: validatorSource(slug), spec }
    const out = await pyRunner.runCases(job, subset, (partial) =>
      setResults((prev) => ({ ...prev, ...Object.fromEntries(partial.map((r) => [r.name, r])) })),
    )
    // Only a run of every test counts as "the solution is done".
    if (subset.length === cases.length) onResults?.(out)
    return { results: out, cases: subset }
  }

  const run = () => void runNames(cases.filter((c) => selected.has(c.name)).map((c) => c.name))
  const toggle = (name: string) =>
    setSelected((s) => {
      const next = new Set(s)
      if (next.has(name)) next.delete(name)
      else next.add(name)
      return next
    })

  const ran = cases.map((c) => results[c.name]).filter((r): r is CaseResult => !!r)
  const passed = ran.filter((r) => r.status === 'pass').length
  const selectedCount = cases.filter((c) => selected.has(c.name)).length

  const editorColumn = (
    <div className="min-w-0 space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <Button size="sm" onClick={run} disabled={busy || selectedCount === 0}>
          <Play /> Run {selectedCount === cases.length ? 'all tests' : `${selectedCount} selected`}{' '}
          <kbd className="ml-1 text-[10px] opacity-70">⌘/Ctrl ↵</kbd>
        </Button>
        <Button size="sm" variant="outline" onClick={() => clearDraft(draftKey)}>
          <RotateCcw /> Reset code
        </Button>
        {toolbar}
        {wide && (
          <div className="ml-auto flex items-center gap-1">
            <Button size="icon" variant="ghost" className="size-8" aria-label={leftCollapsed ? 'Show the notes column' : 'Hide the notes column'}
              title={leftCollapsed ? 'Show notes' : 'Hide notes'}
              onClick={() => (leftPanel.current?.isCollapsed() ? leftPanel.current.expand() : leftPanel.current?.collapse())}>
              {leftCollapsed ? <PanelLeftOpen /> : <PanelLeftClose />}
            </Button>
            <Button size="icon" variant="ghost" className="size-8" aria-label={rightCollapsed ? 'Show the tests column' : 'Hide the tests column'}
              title={rightCollapsed ? 'Show tests' : 'Hide tests'}
              onClick={() => (rightPanel.current?.isCollapsed() ? rightPanel.current.expand() : rightPanel.current?.collapse())}>
              {rightCollapsed ? <PanelRightOpen /> : <PanelRightClose />}
            </Button>
          </div>
        )}
        <span className={`${wide ? '' : 'ml-auto'} text-xs text-muted-foreground`} role="status">
          {STATUS_TEXT[status]}{status === 'error' && pyRunner.detail ? `: ${pyRunner.detail}` : ''}
        </span>
      </div>
      <div className="h-[min(66vh,760px)] min-h-[420px]">
        <CodeEditor value={source} dark={theme === 'dark'} onChange={(v) => setDraft(draftKey, v)} onRun={run} />
      </div>
      {!practice && (
        <Collapsible className="rounded-md border">
          <CollapsibleTrigger className="group flex w-full items-center gap-1.5 px-3 py-2 text-sm font-medium">
            <ChevronRight className="size-4 group-data-[state=open]:hidden" />
            <ChevronDown className="hidden size-4 group-data-[state=open]:block" />
            Benchmark
            <span className="font-normal text-muted-foreground">run the selected tests many times and chart the timings</span>
          </CollapsibleTrigger>
          <CollapsibleContent className="border-t p-3">
            <Benchmark
              disabled={busy || selectedCount === 0}
              runSuite={async () => runNames(cases.filter((c) => selected.has(c.name)).map((c) => c.name))}
            />
          </CollapsibleContent>
        </Collapsible>
      )}
    </div>
  )

  const testsColumn = (
    <div className="min-w-0 space-y-4">
      <section className="space-y-2">
        <h2 className="text-sm font-medium">
          Test cases
          <span className="ml-2 font-normal text-muted-foreground">
            {ran.length > 0 ? `${passed} of ${ran.length} passed · ` : ''}{selectedCount} of {cases.length} selected
          </span>
        </h2>
        <TestsPanel
          spec={spec}
          cases={cases}
          results={results}
          selected={selected}
          running={busy}
          onToggle={toggle}
          onSelectAll={() => setSelected(new Set(cases.map((c) => c.name)))}
          onSelectNone={() => setSelected(new Set())}
          onRunOne={(name) => void runNames([name])}
          hideAfter={practice ? EXAMPLES_SHOWN : undefined}
        />
      </section>
      <section className="rounded-md border p-3">
        <CustomCases slug={slug} spec={spec} />
      </section>
    </div>
  )

  if (!wide) {
    return (
      <div className="space-y-6">
        {left}
        {editorColumn}
        {testsColumn}
      </div>
    )
  }

  return (
    <ResizablePanelGroup orientation="horizontal" className="min-h-[640px] gap-0" style={{ height: 'calc(100vh - 8.5rem)' }}>
      <ResizablePanel
        id="notes"
        panelRef={leftPanel}
        collapsible
        collapsedSize={0}
        defaultSize="22%"
        minSize="14%"
        onResize={() => setLeftCollapsed(!!leftPanel.current?.isCollapsed())}
      >
        <div className="h-full overflow-y-auto pr-4">{left}</div>
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel id="code" defaultSize="48%" minSize="28%">
        <div className="h-full overflow-y-auto px-4">{editorColumn}</div>
      </ResizablePanel>
      <ResizableHandle withHandle />
      <ResizablePanel
        id="tests"
        panelRef={rightPanel}
        collapsible
        collapsedSize={0}
        defaultSize="30%"
        minSize="18%"
        onResize={() => setRightCollapsed(!!rightPanel.current?.isCollapsed())}
      >
        <div className="h-full overflow-y-auto pl-4">{testsColumn}</div>
      </ResizablePanel>
    </ResizablePanelGroup>
  )
}
