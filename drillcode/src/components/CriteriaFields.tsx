import { MultiSelect } from '@/components/MultiSelect'
import { StatusToggle } from '@/components/StatusToggle'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { TOPICS } from '@/lib/catalogue'
import type { StatusFilter } from '@/lib/store'
import type { Difficulty } from '@/lib/types'

export interface Criteria {
  difficulties: Difficulty[]
  topics: string[]
  blind75Only: boolean
  status: StatusFilter
}

/** The "what do you want to work on" fields, shared by the session form and the random walk. */
export function CriteriaFields({ value, onChange }: { value: Criteria; onChange: (patch: Partial<Criteria>) => void }) {
  return (
    <>
      <div className="grid gap-3 sm:grid-cols-2">
        <MultiSelect
          label="Difficulty"
          allLabel="Any difficulty"
          options={['easy', 'medium', 'hard'] as const}
          value={value.difficulties}
          onChange={(difficulties) => onChange({ difficulties })}
          display={(d) => d[0].toUpperCase() + d.slice(1)}
        />
        <MultiSelect label="Topics" allLabel="Any topic" options={TOPICS} value={value.topics} onChange={(topics) => onChange({ topics })} columns={2} />
      </div>
      <div className="space-y-1">
        <Label className="text-xs text-muted-foreground">Which problems</Label>
        <StatusToggle value={value.status} onChange={(status) => onChange({ status })} />
        <p className="text-xs text-muted-foreground">“Done” draws only problems you have ticked off, which is handy for spaced repetition.</p>
      </div>
      <Label className="gap-2 text-sm font-normal">
        <Switch checked={value.blind75Only} onCheckedChange={(blind75Only) => onChange({ blind75Only })} />
        Only the Blind 75
      </Label>
    </>
  )
}

/** "Easy, Medium · Array, String · Not done yet" */
export function describeCriteria(c: Criteria): string {
  const parts = [
    c.difficulties.length ? c.difficulties.map((d) => d[0].toUpperCase() + d.slice(1)).join(', ') : 'Any difficulty',
    c.topics.length ? c.topics.join(', ') : 'Any topic',
    c.status === 'todo' ? 'Not done yet' : c.status === 'done' ? 'Done' : 'Any status',
  ]
  if (c.blind75Only) parts.push('Blind 75')
  return parts.join(' · ')
}
