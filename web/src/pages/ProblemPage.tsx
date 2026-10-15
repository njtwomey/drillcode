import { ArrowLeft, ArrowRight, Eye, ExternalLink } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router'
import { DifficultyBadge } from '@/components/badges'
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
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import { bySlug, definitions, problems, skeletonSource, solutionVariants, testsSpec } from '@/lib/catalogue'
import { draftKey, useStore } from '@/lib/store'
import type { Mode } from '@/lib/types'

export function ProblemPage() {
  const { slug = '' } = useParams()
  if (!bySlug.get(slug) || !testsSpec(slug)) {
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
  const navigate = useNavigate()
  const done = useStore((s) => s.done)
  const queue = useStore((s) => s.queue)
  const { toggleDone, setDraft, setQueuePos } = useStore()

  const [mode, setMode] = useState<Mode>('view')
  const [confirmReveal, setConfirmReveal] = useState(false)
  const variants = useMemo(() => solutionVariants(slug), [slug])
  const [variantId, setVariantId] = useState('primary')
  const variant = variants.find((v) => v.id === variantId) ?? variants[0]

  const neighbours = useMemo(() => {
    const inQueue = queue.indexOf(slug)
    if (inQueue >= 0) return { prev: queue[inQueue - 1], next: queue[inQueue + 1], queued: true }
    const i = problems.findIndex((p) => p.slug === slug)
    return { prev: problems[i - 1]?.slug, next: problems[i + 1]?.slug, queued: false }
  }, [queue, slug])
  function go(target?: string) {
    if (!target) return
    if (neighbours.queued) setQueuePos(queue.indexOf(target))
    navigate(`/p/${target}`)
  }

  const viewing = mode === 'view'
  const defs = definitions(slug)

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-2">
        <h1 className="text-xl font-semibold">{problem.number}. {problem.title}</h1>
        <DifficultyBadge difficulty={problem.difficulty} />
        {viewing && <Badge variant="secondary">{problem.topic}</Badge>}
        {viewing && problem.tags.map((t) => <Badge key={t} variant="outline">{t}</Badge>)}
        <label className="flex items-center gap-1.5 text-sm">
          <Checkbox checked={!!done[slug]} onCheckedChange={() => toggleDone(slug)} /> Done
        </label>
        <div className="ml-auto flex items-center gap-2">
          <ToggleGroup type="single" variant="outline" size="sm" value={mode} onValueChange={(v) => v && setMode(v as Mode)}>
            <ToggleGroupItem value="view">View solution</ToggleGroupItem>
            <ToggleGroupItem value="implement">Implement</ToggleGroupItem>
          </ToggleGroup>
          <Button size="icon" variant="outline" aria-label="Previous problem" disabled={!neighbours.prev} onClick={() => go(neighbours.prev)}><ArrowLeft /></Button>
          <Button size="icon" variant="outline" aria-label="Next problem" disabled={!neighbours.next} onClick={() => go(neighbours.next)}><ArrowRight /></Button>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(260px,320px)_minmax(0,1fr)]">
        <aside className="space-y-4 text-sm">
          <a href={problem.leetcode} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 underline">
            Read the full problem on LeetCode <ExternalLink className="size-3" />
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
              Implement mode hides the approach, tricks and edge cases. Write the solution from the blank
              skeleton, run the tests, and use “Reveal solution” if you get stuck.
            </p>
          )}
          {defs && (
            <div className="rounded-md border p-3">
              <h2 className="mb-2 font-medium">Definitions</h2>
              <pre className="overflow-auto font-mono text-xs">{defs}</pre>
            </div>
          )}
          <p className="text-xs text-muted-foreground">
            {viewing
              ? 'The comment at the top of the code repeats the approach, tricks and edge cases.'
              : 'Your code is saved in this browser as you type.'}
          </p>
        </aside>

        <Workspace
          key={`${mode}-${variant.id}`}
          slug={slug}
          draftKey={draftKey(slug, mode, variant.id)}
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
              {!viewing && (
                <Button size="sm" variant="outline" onClick={() => setConfirmReveal(true)}><Eye /> Reveal solution</Button>
              )}
            </>
          }
        />
      </div>

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
