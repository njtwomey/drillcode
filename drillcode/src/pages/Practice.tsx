import { Footprints, Play, RotateCcw, Trash2 } from 'lucide-react'
import { useMemo } from 'react'
import { useNavigate, useSearchParams } from 'react-router'
import { CriteriaFields } from '@/components/CriteriaFields'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { problems } from '@/lib/catalogue'
import { matchesFilter } from '@/lib/filter'
import { seededShuffle, timeSeed } from '@/lib/random'
import { useStore } from '@/lib/store'

export function Practice() {
  const navigate = useNavigate()
  const [params, setParams] = useSearchParams()
  const config = useStore((s) => s.practiceConfig)
  const walkConfig = useStore((s) => s.walkConfig)
  const done = useStore((s) => s.done)
  const session = useStore((s) => s.practice)
  const walk = useStore((s) => s.walk)
  const { setPracticeConfig, startPractice, discardPractice, setWalkConfig, startWalk, endWalk } = useStore()

  const pool = useMemo(() => problems.filter((p) => matchesFilter(p, config, done)), [config, done])
  const walkPool = useMemo(() => problems.filter((p) => matchesFilter(p, walkConfig, done)), [walkConfig, done])
  const count = Math.min(config.count, pool.length)

  function start() {
    // Seeded from the current time; the seed is kept with the session so its order can be reproduced.
    const seed = timeSeed()
    startPractice(seededShuffle(pool, seed).slice(0, count).map((p) => p.slug), seed)
    navigate('/practice/session')
  }

  function startWalking() {
    const first = seededShuffle(walkPool, timeSeed())[0]
    if (!first) return
    startWalk(first.slug)
    navigate('/practice/walk')
  }

  const unfinished = session && !session.finished ? session : null
  const walkSolved = walk ? Object.values(walk.outcomes).filter((o) => o.status === 'passed').length : 0

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="space-y-1">
        <h1 className="text-xl font-semibold">Practice</h1>
        <p className="text-sm text-muted-foreground">
          Every problem starts from a blank skeleton with no solution, approach or hints, and is checked against the test
          cases. Run a set session, or just keep walking through random problems.
        </p>
      </div>

      <Tabs value={params.get('tab') === 'walk' ? 'walk' : 'session'} onValueChange={(tab) => setParams(tab === 'walk' ? { tab } : {}, { replace: true })}>
        <TabsList>
          <TabsTrigger value="session">Session</TabsTrigger>
          <TabsTrigger value="walk">Random walk</TabsTrigger>
        </TabsList>

        <TabsContent value="session" className="space-y-4">
          {unfinished && (
            <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-muted/40 p-4 text-sm">
              <span>You have a session in progress: problem {unfinished.index + 1} of {unfinished.slugs.length}.</span>
              <div className="ml-auto flex gap-2">
                <Button size="sm" onClick={() => navigate('/practice/session')}><RotateCcw /> Resume</Button>
                <Button size="sm" variant="outline" onClick={discardPractice}><Trash2 /> Discard</Button>
              </div>
            </div>
          )}
          <section className="space-y-4 rounded-lg border p-4">
            <h2 className="text-sm font-medium">New session</h2>
            <p className="text-xs text-muted-foreground">A fixed set of random problems with a summary at the end.</p>
            <CriteriaFields value={config} onChange={setPracticeConfig} />
            <div className="flex flex-wrap items-end gap-4">
              <div className="space-y-1">
                <Label htmlFor="count" className="text-xs text-muted-foreground">How many problems</Label>
                <Input
                  id="count" type="number" min={1} max={50} className="h-8 w-24" value={config.count}
                  onChange={(e) => setPracticeConfig({ count: Math.max(1, Math.min(50, Number(e.target.value) || 1)) })}
                />
              </div>
              <Button onClick={start} disabled={pool.length === 0}>
                <Play /> Start session{pool.length > 0 ? ` (${count})` : ''}
              </Button>
              <span className="text-sm text-muted-foreground">
                {pool.length === 0 ? 'No problems match these settings.' : `${pool.length} problems match`}
              </span>
            </div>
          </section>
        </TabsContent>

        <TabsContent value="walk" className="space-y-4">
          {walk && (
            <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-muted/40 p-4 text-sm">
              <span>Your walk is in progress: {walk.history.length} visited, {walkSolved} solved.</span>
              <div className="ml-auto flex gap-2">
                <Button size="sm" onClick={() => navigate('/practice/walk')}><Footprints /> Continue</Button>
                <Button size="sm" variant="outline" onClick={endWalk}><Trash2 /> End walk</Button>
              </div>
            </div>
          )}
          <section className="space-y-4 rounded-lg border p-4">
            <h2 className="text-sm font-medium">{walk ? 'Criteria for the next random problem' : 'Start a random walk'}</h2>
            <p className="text-xs text-muted-foreground">
              No count and no end. Set a loose theme, then press “Next random” whenever you want another problem that
              matches. Problems you have not seen in this walk come first. Your place is kept, so you can stop and come back.
              {walk ? ' Changes here apply from the next problem.' : ''}
            </p>
            <CriteriaFields value={walkConfig} onChange={setWalkConfig} />
            <div className="flex flex-wrap items-center gap-4">
              <Button onClick={startWalking} disabled={walkPool.length === 0} variant={walk ? 'outline' : 'default'}>
                <Footprints /> {walk ? 'Start a fresh walk' : 'Start walking'}
              </Button>
              <span className="text-sm text-muted-foreground">
                {walkPool.length === 0 ? 'No problems match these settings.' : `${walkPool.length} problems match`}
              </span>
            </div>
          </section>
        </TabsContent>
      </Tabs>
    </div>
  )
}
