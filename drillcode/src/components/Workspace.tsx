import { ChevronDown, ChevronRight, PanelLeftClose, PanelLeftOpen, PanelRightClose, PanelRightOpen, Play, RotateCcw } from 'lucide-react'
import { useEffect, useRef, useState, useSyncExternalStore, type ReactNode } from 'react'
import { usePanelRef } from 'react-resizable-panels'
import { Benchmark } from '@/components/Benchmark'
import { CodeEditor } from '@/components/CodeEditor'
import { CaseForm, CustomCases } from '@/components/CustomCases'
import { TestsPanel } from '@/components/TestsPanel'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable'
import { solutionVariants, testsSpec, validatorSource } from '@/lib/catalogue'
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
  /** Exposure, the only thing that differs between views: how many catalogue cases are shown. The rest stay hidden. Undefined shows all. */
  visibleExamples?: number
  /** Called only after a run that covered every test case. */
  onResults?: (results: CaseResult[]) => void
}

/** What makes a case's run result stale: its input and its expected value. */
const fingerprint = (c: TestCase) => JSON.stringify([c.input, c.ops, c.expected])

/**
 * Three columns: notes | code | tests. The side columns collapse and drag. Each test can be ticked,
 * run alone, opened, and carries its own console output; Run runs whatever is ticked.
 */
export function Workspace({ slug, draftKey, originalSource, left, toolbar, visibleExamples, onResults }: Props) {
  const spec = testsSpec(slug)!
  const drafts = useStore((s) => s.drafts)
  const theme = useStore((s) => s.theme)
  const custom = useStore((s) => s.customCases[slug]) ?? NONE
  const { setDraft, clearDraft, updateCustomCase, removeCustomCase } = useStore()
  const [editing, setEditing] = useState<string | null>(null)
  // The case whose error line is marked in the editor (null: none). Cleared as soon as the code changes.
  const [errorCase, setErrorCase] = useState<string | null>(null)
  const status = useSyncExternalStore(pyRunner.subscribe, pyRunner.getSnapshot)
  const wide = useIsWide()

  const [results, setResults] = useState<Record<string, CaseResult | undefined>>({})
  const [selected, setSelected] = useState<Set<string>>(() => new Set(spec.cases.map((c) => c.name)))
  const leftPanel = usePanelRef()
  const rightPanel = usePanelRef()
  const [leftCollapsed, setLeftCollapsed] = useState(false)
  const [rightCollapsed, setRightCollapsed] = useState(false)

  const source = drafts[draftKey] ?? originalSource
  useEffect(() => setErrorCase(null), [source])
  // Cases you added come first, newest at the top, so a new one is right where you are looking.
  const cases = [...custom.map((c) => ({ ...c, custom: true })).reverse(), ...spec.cases]
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
    const referenceSource = solutionVariants(slug)[0].source
    const job = { solutionSource: source, validatorSource: validatorSource(slug), referenceSource, spec }
    const out = await pyRunner.runCases(job, subset, (partial) =>
      setResults((prev) => ({ ...prev, ...Object.fromEntries(partial.map((r) => [r.name, r])) })),
    )
    // A case added without an expected value now has one, from the reference solution: keep it so it shows in the list.
    for (const r of out) {
      if (r.expected_source === 'reference' && subset.find((c) => c.name === r.name)?.custom) {
        const c = subset.find((x) => x.name === r.name)!
        lastRun.current.set(r.name, fingerprint({ ...c, expected: r.expected }))
        updateCustomCase(slug, r.name, { expected: r.expected, derived: true })
      }
    }
    // An error points at a line of your code: mark the first one, so you see where it happened.
    const broken = out.find((r) => (r.status === 'error' || r.status === 'timeout') && r.error_line)
    setErrorCase(broken ? broken.name : null)
    // Only a run of every test counts as "the solution is done".
    if (subset.length === cases.length) onResults?.(out)
    return { results: out, cases: subset }
  }

  // A case you add or edit runs straight away (just that case), so you see its result without pressing anything.
  // The cases already there when the page opens are not re-run.
  const lastRun = useRef<Map<string, string>>(new Map(custom.map((c) => [c.name, fingerprint(c)])))
  useEffect(() => {
    if (status !== 'ready') return
    for (const c of cases) {
      if (!c.custom) continue
      const f = fingerprint(c)
      if (lastRun.current.get(c.name) === f) continue
      lastRun.current.set(c.name, f)
      void runNames([c.name])
      return // one at a time; the next render picks up any others
    }
  })

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
        <CodeEditor value={source} dark={theme === 'dark'} errorLine={errorCase ? results[errorCase]?.error_line : null} onChange={(v) => setDraft(draftKey, v)} onRun={run} />
      </div>
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
    </div>
  )

  const testsColumn = (
    <div className="min-w-0 space-y-4">
      <CustomCases slug={slug} spec={spec} />
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
          onSelectMine={() => setSelected(new Set(custom.map((c) => c.name)))}
          onRunOne={(name) => void runNames([name])}
          editing={editing}
          onEdit={setEditing}
          onDelete={(name) => {
            lastRun.current.delete(name)
            if (editing === name) setEditing(null)
            removeCustomCase(slug, name)
          }}
          renderEditor={(c) => (
            <CaseForm slug={slug} spec={spec} initial={c} onDone={() => setEditing(null)} />
          )}
          visibleExamples={visibleExamples}
          errorCase={errorCase}
          onShowError={setErrorCase}
        />
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
