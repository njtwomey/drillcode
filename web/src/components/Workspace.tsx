import { Play, RotateCcw } from 'lucide-react'
import { useState, useSyncExternalStore, type ReactNode } from 'react'
import { Benchmark } from '@/components/Benchmark'
import { CodeEditor } from '@/components/CodeEditor'
import { CustomCases } from '@/components/CustomCases'
import { TestsPanel } from '@/components/TestsPanel'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { testsSpec, validatorSource } from '@/lib/catalogue'
import { useStore } from '@/lib/store'
import type { CaseResult, TestCase } from '@/lib/types'
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
  /** Extra toolbar controls (approach picker, Reveal). */
  toolbar?: ReactNode
  /** Practice: hide case names after the examples, no benchmark. */
  practice?: boolean
  onResults?: (results: CaseResult[]) => void
}

const EXAMPLES_SHOWN = 2

/** The editor with its toolbar, plus Tests / Console / Custom cases / Benchmark underneath. */
export function Workspace({ slug, draftKey, originalSource, toolbar, practice, onResults }: Props) {
  const spec = testsSpec(slug)!
  const drafts = useStore((s) => s.drafts)
  const theme = useStore((s) => s.theme)
  const custom = useStore((s) => s.customCases[slug]) ?? NONE
  const { setDraft, clearDraft } = useStore()
  const status = useSyncExternalStore(pyRunner.subscribe, pyRunner.getSnapshot)
  const [results, setResults] = useState<CaseResult[]>([])
  const [tab, setTab] = useState('tests')

  const source = drafts[draftKey] ?? originalSource
  const cases = [...spec.cases, ...custom.map((c) => ({ ...c, custom: true }))]
  const busy = status === 'running' || status === 'error'

  // CodeEditor keeps its onRun callback current, so these closures always see the latest text.
  async function runSuite(onProgress?: (r: CaseResult[]) => void) {
    const job = { solutionSource: source, validatorSource: validatorSource(slug), spec }
    return { results: await pyRunner.runCases(job, cases, onProgress), cases }
  }

  async function run() {
    if (busy) return
    setResults([])
    setTab('tests')
    const out = await runSuite(setResults)
    onResults?.(out.results)
  }

  const passed = results.filter((r) => r.status === 'pass').length
  const consoleText = results
    .map((r) => {
      const body = [r.stdout, r.stderr, r.status === 'error' || r.status === 'timeout' ? r.message : '']
        .filter((s) => s && s.trim())
        .join('\n')
      return body ? `# ${r.name}\n${body.trimEnd()}` : ''
    })
    .filter(Boolean)
    .join('\n\n')

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <Button size="sm" onClick={run} disabled={busy}>
          <Play /> Run tests <kbd className="ml-1 text-[10px] opacity-70">⌘/Ctrl ↵</kbd>
        </Button>
        <Button size="sm" variant="outline" onClick={() => clearDraft(draftKey)}>
          <RotateCcw /> Reset code
        </Button>
        {toolbar}
        <span className="ml-auto text-xs text-muted-foreground" role="status">
          {STATUS_TEXT[status]}{status === 'error' && pyRunner.detail ? `: ${pyRunner.detail}` : ''}
        </span>
      </div>
      <div className="h-[min(68vh,760px)] min-h-[440px]">
        <CodeEditor value={source} dark={theme === 'dark'} onChange={(v) => setDraft(draftKey, v)} onRun={run} />
      </div>

      <Tabs value={tab} onValueChange={setTab}>
        <TabsList>
          <TabsTrigger value="tests">
            Test cases{results.length > 0 ? ` · ${passed}/${results.length} passed` : ` · ${cases.length}`}
          </TabsTrigger>
          <TabsTrigger value="console">Console</TabsTrigger>
          <TabsTrigger value="custom">Add a case</TabsTrigger>
          {!practice && <TabsTrigger value="benchmark">Benchmark</TabsTrigger>}
        </TabsList>
        <TabsContent value="tests">
          <TestsPanel spec={spec} cases={cases} results={results} hideAfter={practice ? EXAMPLES_SHOWN : undefined} />
        </TabsContent>
        <TabsContent value="console">
          <pre className="max-h-64 overflow-auto rounded-md border bg-muted/40 p-3 font-mono text-xs whitespace-pre-wrap">
            {consoleText || 'print() output, errors and tracebacks appear here after a run.'}
          </pre>
        </TabsContent>
        <TabsContent value="custom">
          <CustomCases slug={slug} spec={spec} />
        </TabsContent>
        {!practice && (
          <TabsContent value="benchmark">
            <Benchmark
              disabled={busy}
              runSuite={async () => {
                const out = await runSuite()
                setResults(out.results)
                return out
              }}
            />
          </TabsContent>
        )}
      </Tabs>
    </div>
  )
}
