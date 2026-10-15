import { ArrowLeft, ArrowRight, Eye, ExternalLink, Play, RotateCcw } from 'lucide-react'
import { useMemo, useState, useSyncExternalStore } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import { Benchmark } from '@/components/Benchmark'
import { CodeEditor } from '@/components/CodeEditor'
import { CustomCases } from '@/components/CustomCases'
import { Console, ResultsTable } from '@/components/ResultsPanel'
import { DifficultyBadge } from '@/components/badges'
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import {
  bySlug, definitions, problems, skeletonSource, solutionVariants, testsSpec, validatorSource,
} from '@/lib/catalogue'
import { draftKey, useStore } from '@/lib/store'
import type { CaseResult, Mode, TestCase } from '@/lib/types'
import { pyRunner } from '@/py/runner'

const NONE: TestCase[] = []
const STATUS_TEXT = {
  loading: 'Loading Pyodide…',
  ready: 'Python ready',
  running: 'Running…',
  restarting: 'Restarting Python after a timeout…',
  error: 'Python failed to load',
} as const

export function ProblemPage() {
  const { slug = '' } = useParams()
  const problem = bySlug.get(slug)
  const spec = testsSpec(slug)
  if (!problem || !spec) {
    return (
      <p className="text-sm">
        Unknown or unfinished problem “{slug}”. <Link className="underline" to="/">Back to the list</Link>
      </p>
    )
  }
  return <ProblemView key={slug} slug={slug} />
}

function ProblemView({ slug }: { slug: string }) {
  const problem = bySlug.get(slug)!
  const spec = testsSpec(slug)!
  const navigate = useNavigate()
  const { done, drafts, queue, theme, toggleDone, setDraft, clearDraft, setQueuePos } = useStore()
  const custom = useStore((s) => s.customCases[slug]) ?? NONE
  const status = useSyncExternalStore(pyRunner.subscribe, pyRunner.getSnapshot)

  const [mode, setMode] = useState<Mode>('view')
  const [results, setResults] = useState<CaseResult[]>([])
  const [confirmReveal, setConfirmReveal] = useState(false)

  const variants = useMemo(() => solutionVariants(slug), [slug])
  const [variantId, setVariantId] = useState('primary')
  const variant = variants.find((v) => v.id === variantId) ?? variants[0]
  const key = draftKey(slug, mode, variant.id)
  const original = mode === 'view' ? variant.source : skeletonSource(slug)
  const source = drafts[key] ?? original

  // CodeEditor keeps its onRun callback current, so these closures always see the latest text.
  async function runSuite(onProgress?: (r: CaseResult[]) => void) {
    const cases = [...spec.cases, ...custom.map((c) => ({ ...c, custom: true }))]
    const job = { solutionSource: source, validatorSource: validatorSource(slug), spec }
    return { results: await pyRunner.runCases(job, cases, onProgress), cases }
  }

  async function run() {
    if (pyRunner.status === 'running' || pyRunner.status === 'error') return
    setResults([])
    await runSuite(setResults)
  }

  const neighbours = useMemo(() => {
    const inQueue = queue.indexOf(slug)
    if (inQueue >= 0) return { prev: queue[inQueue - 1], next: queue[inQueue + 1], queued: true, pos: inQueue }
    const i = problems.findIndex((p) => p.slug === slug)
    return { prev: problems[i - 1]?.slug, next: problems[i + 1]?.slug, queued: false, pos: i }
  }, [queue, slug])
  function go(target?: string) {
    if (!target) return
    if (neighbours.queued) setQueuePos(queue.indexOf(target))
    navigate(`/p/${target}`)
  }

  const defs = definitions(slug)

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <h1 className="text-lg font-semibold">{problem.number}. {problem.title}</h1>
        <DifficultyBadge difficulty={problem.difficulty} />
        <Badge variant="secondary">{problem.topic}</Badge>
        {problem.tags.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}
        <span className="text-xs text-muted-foreground">
          time {problem.complexity.time} · space {problem.complexity.space}
        </span>
        <a href={problem.leetcode} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-xs underline">
          LeetCode <ExternalLink className="size-3" />
        </a>
        <label className="flex items-center gap-1.5 text-sm">
          <Checkbox checked={!!done[slug]} onCheckedChange={() => toggleDone(slug)} /> Done
        </label>
        <div className="ml-auto flex items-center gap-2">
          <ToggleGroup type="single" variant="outline" size="sm" value={mode} onValueChange={(v) => v && setMode(v as Mode)}>
            <ToggleGroupItem value="view">View</ToggleGroupItem>
            <ToggleGroupItem value="implement">Implement</ToggleGroupItem>
          </ToggleGroup>
          <Button size="icon" variant="outline" aria-label="Previous" disabled={!neighbours.prev} onClick={() => go(neighbours.prev)}><ArrowLeft /></Button>
          <Button size="icon" variant="outline" aria-label="Next" disabled={!neighbours.next} onClick={() => go(neighbours.next)}><ArrowRight /></Button>
        </div>
      </div>

      <div className="grid gap-3 lg:grid-cols-[minmax(0,1fr)_minmax(0,1.4fr)]">
        <div className="space-y-3">
          <Tabs defaultValue="summary" className="rounded-md border p-3">
            <TabsList>
              <TabsTrigger value="summary">Summary</TabsTrigger>
              <TabsTrigger value="tricks">Tricks</TabsTrigger>
              <TabsTrigger value="edge">Edge cases</TabsTrigger>
            </TabsList>
            <TabsContent value="summary" className="text-sm">{problem.summary}</TabsContent>
            <TabsContent value="tricks" className="text-sm">{problem.tricks}</TabsContent>
            <TabsContent value="edge" className="text-sm">
              <ul className="list-disc pl-5">{problem.edge_cases.map((e) => <li key={e}>{e}</li>)}</ul>
            </TabsContent>
          </Tabs>
          {defs && (
            <Collapsible className="rounded-md border p-3">
              <CollapsibleTrigger className="text-sm font-medium">Definitions</CollapsibleTrigger>
              <CollapsibleContent>
                <pre className="mt-2 overflow-auto font-mono text-xs">{defs}</pre>
              </CollapsibleContent>
            </Collapsible>
          )}
          <div className="rounded-md border p-3">
            <h2 className="mb-2 text-sm font-medium">Custom edge cases</h2>
            <CustomCases slug={slug} spec={spec} />
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <Button size="sm" onClick={run} disabled={status === 'running' || status === 'error'}>
              <Play /> Run tests <kbd className="ml-1 text-[10px] opacity-70">⌘/Ctrl ↵</kbd>
            </Button>
            {variants.length > 1 && (
              <Select value={variant.id} onValueChange={setVariantId}>
                <SelectTrigger size="sm" className="w-44" aria-label="Solution approach"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {variants.map((v) => <SelectItem key={v.id} value={v.id} className="capitalize">{v.label}</SelectItem>)}
                </SelectContent>
              </Select>
            )}
            {mode === 'implement' && (
              <Button size="sm" variant="outline" onClick={() => setConfirmReveal(true)}><Eye /> Reveal solution</Button>
            )}
            <Button size="sm" variant="outline" onClick={() => clearDraft(key)}><RotateCcw /> Reset</Button>
            <span className="ml-auto text-xs text-muted-foreground" role="status">
              {STATUS_TEXT[status]}{status === 'error' && pyRunner.detail ? `: ${pyRunner.detail}` : ''}
            </span>
          </div>
          <div className="h-[420px]">
            <CodeEditor value={source} dark={theme === 'dark'} onChange={(v) => setDraft(key, v)} onRun={run} />
          </div>
        </div>
      </div>

      {results.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">
            {results.filter((r) => r.status === 'pass').length} of {results.length} passed
          </p>
          <ResultsTable results={results} />
        </div>
      )}
      <Console results={results} />
      <Benchmark
        disabled={status === 'running' || status === 'error'}
        runSuite={async () => {
          const out = await runSuite()
          setResults(out.results)
          return out
        }}
      />

      <AlertDialog open={confirmReveal} onOpenChange={setConfirmReveal}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reveal the solution?</AlertDialogTitle>
            <AlertDialogDescription>This replaces what is in the editor with the reference solution.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={() => setDraft(draftKey(slug, 'implement'), variant.source)}>Reveal</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
