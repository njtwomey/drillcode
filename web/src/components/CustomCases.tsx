import { Plus, Trash2 } from 'lucide-react'
import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { caseHelp, formatCase, parseCaseLine } from '@/lib/caseFormat'
import { useStore } from '@/lib/store'
import type { TestCase, TestsSpec } from '@/lib/types'

const NONE: TestCase[] = []

/** One field: write the call the way the tests list it, e.g. `[-1,0,3,5,9], 9 → 4`. */
export function CustomCases({ slug, spec }: { slug: string; spec: TestsSpec }) {
  const cases = useStore((s) => s.customCases[slug]) ?? NONE
  const { addCustomCase, removeCustomCase } = useStore()
  const [text, setText] = useState('')
  const parsed = text.trim() ? parseCaseLine(spec, text) : null
  const example = formatCase(spec, spec.cases[0])

  function add() {
    if (!parsed?.case) return
    const used = new Set(cases.map((c) => c.name))
    let n = cases.length + 1
    while (used.has(`my case ${n}`)) n++
    addCustomCase(slug, { name: `my case ${n}`, ...parsed.case })
    setText('')
  }

  return (
    <div className="space-y-3 text-sm">
      <div className="space-y-1.5">
        <Label htmlFor="custom-case">Add your own test case</Label>
        <div className="flex gap-2">
          <Input
            id="custom-case"
            className="font-mono text-xs"
            placeholder={example}
            value={text}
            spellCheck={false}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && add()}
          />
          <Button size="sm" onClick={add} disabled={!parsed?.case}>
            <Plus /> Add
          </Button>
        </div>
        <p className="text-xs text-muted-foreground">{caseHelp(spec)}</p>
        {parsed?.error && <p className="text-xs text-destructive">{parsed.error}</p>}
        {parsed?.case && <p className="text-xs text-green-700 dark:text-green-400">Looks good. Press Enter or Add.</p>}
      </div>
      {cases.length > 0 && (
        <ul className="divide-y rounded-md border">
          {cases.map((c) => (
            <li key={c.name} className="flex items-center justify-between gap-2 px-3 py-1.5">
              <span className="min-w-0 truncate">
                <Badge variant="outline" className="mr-2">custom</Badge>
                <span className="font-mono text-xs">{formatCase(spec, c)}</span>
              </span>
              <Button size="icon" variant="ghost" aria-label={`Delete ${c.name}`} onClick={() => removeCustomCase(slug, c.name)}>
                <Trash2 />
              </Button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
