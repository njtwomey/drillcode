import { Play, RotateCcw, Trash2 } from 'lucide-react'
import { useMemo } from 'react'
import { useNavigate } from 'react-router'
import { MultiSelect } from '@/components/MultiSelect'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { problems, TOPICS } from '@/lib/catalogue'
import { matchesFilter } from '@/lib/filter'
import { useStore } from '@/lib/store'

export function Practice() {
  const navigate = useNavigate()
  const config = useStore((s) => s.practiceConfig)
  const done = useStore((s) => s.done)
  const session = useStore((s) => s.practice)
  const { setPracticeConfig, startPractice, discardPractice } = useStore()

  const pool = useMemo(
    () => problems.filter((p) => matchesFilter(p, config) && !(config.skipDone && done[p.slug])),
    [config, done],
  )
  const count = Math.min(config.count, pool.length)

  function start() {
    const slugs = [...pool]
    for (let i = slugs.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[slugs[i], slugs[j]] = [slugs[j], slugs[i]]
    }
    startPractice(slugs.slice(0, count).map((p) => p.slug))
    navigate('/practice/session')
  }

  const unfinished = session && !session.finished ? session : null

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="space-y-1">
        <h1 className="text-xl font-semibold">Practice</h1>
        <p className="text-sm text-muted-foreground">
          Pick what you want to work on and get a random set of problems. Each one starts from a blank
          skeleton with no solution, approach or hints, and is checked against the test cases.
        </p>
      </div>

      {unfinished && (
        <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-muted/40 p-4 text-sm">
          <span>
            You have a session in progress: problem {unfinished.index + 1} of {unfinished.slugs.length}.
          </span>
          <div className="ml-auto flex gap-2">
            <Button size="sm" onClick={() => navigate('/practice/session')}><RotateCcw /> Resume</Button>
            <Button size="sm" variant="outline" onClick={discardPractice}><Trash2 /> Discard</Button>
          </div>
        </div>
      )}

      <section className="space-y-4 rounded-lg border p-4">
        <h2 className="text-sm font-medium">New session</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <MultiSelect
            label="Difficulty"
            allLabel="Any difficulty"
            options={['easy', 'medium', 'hard'] as const}
            value={config.difficulties}
            onChange={(difficulties) => setPracticeConfig({ difficulties })}
            display={(d) => d[0].toUpperCase() + d.slice(1)}
          />
          <MultiSelect
            label="Topics"
            allLabel="Any topic"
            options={TOPICS}
            value={config.topics}
            onChange={(topics) => setPracticeConfig({ topics })}
            columns={2}
          />
        </div>
        <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-sm">
          <Label className="gap-2 font-normal">
            <Switch checked={config.blind75Only} onCheckedChange={(blind75Only) => setPracticeConfig({ blind75Only })} />
            Only the Blind 75
          </Label>
          <Label className="gap-2 font-normal">
            <Switch checked={config.skipDone} onCheckedChange={(skipDone) => setPracticeConfig({ skipDone })} />
            Skip problems I’ve done
          </Label>
        </div>
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
    </div>
  )
}
