import { ArrowLeft, ArrowRight, Eye, ExternalLink, Pencil, Play } from 'lucide-react'
import { useMemo, useRef, useState } from 'react'
import { Link, NavLink, useNavigate, useParams } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
import { Description } from '@/components/Description'
import { Markdown } from '@/components/Markdown'
import { WalkthroughDialog } from '@/components/WalkthroughDialog'
import { Workspace } from '@/components/Workspace'
import {
  AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription,
  AlertDialogFooter, AlertDialogHeader, AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  bySlug, definitions, descriptionSource, hasWalkthrough, problems, skeletonSource, solutionVariants, testsSpec,
} from '@/lib/catalogue'
import { formatDuration } from '@/lib/format'
import { formatAgo, solveStats } from '@/lib/stats'
import { draftKey, useStore } from '@/lib/store'
import { techniquesForProblem } from '@/lib/techniques'
import { useWalkthrough } from '@/lib/useWalkthrough'
import type { CaseResult } from '@/lib/types'
import { cn } from '@/lib/utils'

/** The three pages of a problem: /p/:slug/view, /p/:slug/impl and /p/:slug/read. */
export type PageMode = 'view' | 'impl' | 'read'

export function ProblemPage({ mode }: { mode: PageMode }) {
  const { slug = '' } = useParams()
  if (!bySlug.get(slug) || !testsSpec(slug)) {
    return (
      <p className="text-sm">
        Unknown or unfinished problem “{slug}”. <Link className="underline" to="/problems">Back to the problems</Link>
      </p>
    )
  }
  return <ProblemView key={`${slug}-${mode}`} slug={slug} mode={mode} />
}

const TABS: { mode: PageMode; label: string }[] = [
  { mode: 'view', label: 'View solution' },
  { mode: 'impl', label: 'Implement' },
  { mode: 'read', label: 'Read' },
]

function ProblemView({ slug, mode }: { slug: string; mode: PageMode }) {
  const problem = bySlug.get(slug)!
  const navigate = useNavigate()
  const done = useStore((s) => s.done)
  const solves = useStore((s) => s.solves)
  const { toggleDone, setDraft, recordSolve } = useStore()
  const stats = useMemo(() => solveStats(solves).get(slug), [solves, slug])
  // One solve per visit to the Implement page, however many times the passing code is re-run.
  const recorded = useRef(false)

  const [confirmReveal, setConfirmReveal] = useState(false)
  const variants = useMemo(() => solutionVariants(slug), [slug])
  const [variantId, setVariantId] = useState('primary')
  const variant = variants.find((v) => v.id === variantId) ?? variants[0]

  // Previous and next follow the catalogue order and stay on the same kind of page.
  const index = problems.findIndex((p) => p.slug === slug)
  const prev = problems[index - 1]?.slug
  const next = problems[index + 1]?.slug
  const go = (target?: string) => target && navigate(`/p/${target}/${mode}`)

  const implementing = mode === 'impl'
  const viewing = mode === 'view'
  const tips = techniquesForProblem(slug)
  const defs = definitions(slug)
  const description = descriptionSource(slug)
  const { text: walkthrough, loading: walkthroughLoading } = useWalkthrough(slug, mode === 'read')
  const storeMode = implementing ? 'implement' : 'view'

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <h1 className="text-xl font-semibold">{problem.number}. {problem.title}</h1>
        <DifficultyBadge difficulty={problem.difficulty} />
        {!implementing && <Badge variant="secondary">{problem.topic}</Badge>}
        {!implementing && problem.tags.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}
        <label className="flex items-center gap-1.5 text-sm">
          <Checkbox checked={!!done[slug]} onCheckedChange={() => toggleDone(slug)} /> Done
        </label>
        {stats && (
          <span className="text-xs text-muted-foreground">
            Solved {stats.count} time{stats.count === 1 ? '' : 's'} · last {formatAgo(stats.last)}
            {stats.bestSeconds !== undefined && ` · best ${formatDuration(stats.bestSeconds)}`}
          </span>
        )}
        <div className="ml-auto flex items-center gap-2">
          <nav className="inline-flex rounded-md border p-0.5 text-sm" aria-label="Problem pages">
            {TABS.map((t) => (
              <NavLink
                key={t.mode}
                to={`/p/${slug}/${t.mode}`}
                className={({ isActive }) =>
                  cn('rounded px-3 py-1', isActive ? 'bg-primary text-primary-foreground' : 'text-muted-foreground hover:text-foreground')
                }
              >
                {t.label}
              </NavLink>
            ))}
          </nav>
          <Button size="icon" variant="outline" aria-label="Previous problem" disabled={!prev} onClick={() => go(prev)}><ArrowLeft /></Button>
          <Button size="icon" variant="outline" aria-label="Next problem" disabled={!next} onClick={() => go(next)}><ArrowRight /></Button>
        </div>
      </div>

      {!implementing && tips.length > 0 && (
        <div className="flex flex-wrap items-center gap-2 text-sm">
          <span className="text-muted-foreground">Techniques:</span>
          {tips.map((t) => (
            <Link key={t.slug} to={`/tips/${t.slug}`}><Badge variant="outline" className="hover:bg-muted">{t.title}</Badge></Link>
          ))}
        </div>
      )}

      {mode === 'read' ? (
        <article className="mx-auto max-w-3xl space-y-6">
          <section className="space-y-3 rounded-lg border p-4 text-sm">
            {description && <Description source={description} slug={slug} />}
            <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
              <span>Time {problem.complexity.time} · space {problem.complexity.space}</span>
              <a href={problem.leetcode} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 underline">
                Full statement on LeetCode <ExternalLink className="size-3" />
              </a>
            </div>
          </section>
          {walkthrough ? (
            <Markdown source={walkthrough} />
          ) : walkthroughLoading ? (
            <p className="text-sm text-muted-foreground">Loading the walkthrough…</p>
          ) : (
            <p className="text-sm text-muted-foreground">
              {hasWalkthrough(slug) ? 'The walkthrough could not be loaded.' : 'No walkthrough has been written for this problem yet.'}
            </p>
          )}
          <div className="flex flex-wrap gap-2 border-t pt-4">
            <Button asChild size="sm"><Link to={`/p/${slug}/impl`}><Pencil /> Try it yourself</Link></Button>
            <Button asChild size="sm" variant="outline"><Link to={`/p/${slug}/view`}><Play /> See the code and run it</Link></Button>
          </div>
        </article>
      ) : (
        <div>
          <Workspace
            left={
          <aside className="space-y-4 text-sm">
              {description && <Description source={description} slug={slug} />}
              <a href={problem.leetcode} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 underline">
                Full statement on LeetCode <ExternalLink className="size-3" />
              </a>
              {viewing ? (
                <Tabs defaultValue="summary" className="rounded-md border p-3">
                  <TabsList>
                    <TabsTrigger value="summary">Approach</TabsTrigger>
                    <TabsTrigger value="tricks">Tricks</TabsTrigger>
                    <TabsTrigger value="edge">Edge cases</TabsTrigger>
                  </TabsList>
                  <TabsContent value="summary" className="space-y-2">
                    <p>{problem.summary}</p>
                    <p className="text-xs text-muted-foreground">Time {problem.complexity.time} · space {problem.complexity.space}</p>
                  </TabsContent>
                  <TabsContent value="tricks">{problem.tricks}</TabsContent>
                  <TabsContent value="edge">
                    <ul className="list-disc space-y-1 pl-5">{problem.edge_cases.map((e) => <li key={e}>{e}</li>)}</ul>
                  </TabsContent>
                </Tabs>
              ) : (
                <p className="rounded-md border p-3 text-muted-foreground">
                  This page hides the approach, tricks, edge cases and walkthrough. Write the solution from the blank
                  skeleton, run the tests, and use “Reveal solution” if you get stuck.
                </p>
              )}
              {defs && (
                <div className="rounded-md border p-3">
                  <h2 className="mb-2 font-medium">Definitions and judge notes</h2>
                  <pre className="overflow-auto font-mono text-xs">{defs}</pre>
                </div>
              )}
              <p className="text-xs text-muted-foreground">
                {viewing
                  ? 'The comment at the top of the code repeats the approach, tricks and edge cases.'
                  : 'Your code is saved in this browser as you type.'}
              </p>
            </aside>
            }
            key={`${mode}-${variant.id}`}
            slug={slug}
            onResults={(results: CaseResult[]) => {
              const passed = results.length > 0 && results.every((r) => r.status === 'pass')
              if (implementing && passed && !recorded.current) {
                recorded.current = true
                recordSolve({ slug, source: 'implement' })
              }
            }}
            draftKey={draftKey(slug, storeMode, variant.id)}
            originalSource={viewing ? variant.source : skeletonSource(slug)}
            toolbar={
              <>
                {viewing && variants.length > 1 && (
                  <Select value={variant.id} onValueChange={setVariantId}>
                    <SelectTrigger size="sm" className="w-44" aria-label="Solution approach"><SelectValue /></SelectTrigger>
                    <SelectContent>
                      {variants.map((v) => <SelectItem key={v.id} value={v.id} className="capitalize">{v.label}</SelectItem>)}
                    </SelectContent>
                  </Select>
                )}
                {viewing && <WalkthroughDialog slug={slug} title={problem.title} />}
                {implementing && (
                  <Button size="sm" variant="outline" onClick={() => setConfirmReveal(true)}><Eye /> Reveal solution</Button>
                )}
              </>
            }
          />
        </div>
      )}

      <AlertDialog open={confirmReveal} onOpenChange={setConfirmReveal}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reveal the solution?</AlertDialogTitle>
            <AlertDialogDescription>This replaces what is in the editor with the reference solution.</AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction onClick={() => setDraft(draftKey(slug, 'implement'), variants[0].source)}>Reveal</AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  )
}
