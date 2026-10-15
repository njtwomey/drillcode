import { Trash2 } from 'lucide-react'
import { useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { useStore } from '@/lib/store'
import type { TestCase, TestsSpec } from '@/lib/types'

const NONE: TestCase[] = []

function parseJson(text: string, label: string): { value?: unknown; error?: string } {
  try {
    return { value: JSON.parse(text) }
  } catch (e) {
    return { error: `${label} is not valid JSON: ${(e as Error).message}` }
  }
}

export function CustomCases({ slug, spec }: { slug: string; spec: TestsSpec }) {
  const cases = useStore((s) => s.customCases[slug]) ?? NONE
  const { addCustomCase, removeCustomCase } = useStore()
  const isOps = spec.kind === 'operations'
  const template = isOps
    ? spec.cases[0]?.ops
    : Object.fromEntries((spec.args ?? []).map((a) => [a, spec.cases[0]?.input?.[a] ?? null]))
  const [name, setName] = useState('')
  const [input, setInput] = useState('')
  const [expected, setExpected] = useState('')
  const [error, setError] = useState('')

  function save() {
    if (!name.trim()) return setError('Give the case a name.')
    const parsedInput = parseJson(input, isOps ? 'Ops' : 'Input')
    if (parsedInput.error) return setError(parsedInput.error)
    const parsedExpected = parseJson(expected, 'Expected')
    if (parsedExpected.error) return setError(parsedExpected.error)
    const value = parsedInput.value
    if (isOps) {
      const ok = Array.isArray(value) && value.length > 0 && value.every((op) => Array.isArray(op) && typeof op[0] === 'string' && Array.isArray(op[1]))
      if (!ok) return setError('Ops must be a list of [name, [args...]] pairs.')
    } else {
      if (typeof value !== 'object' || value === null || Array.isArray(value)) return setError('Input must be a JSON object.')
      const missing = (spec.args ?? []).filter((a) => !(a in (value as object)))
      if (missing.length) return setError(`Input is missing: ${missing.join(', ')}`)
    }
    addCustomCase(slug, {
      name: name.trim(),
      custom: true,
      expected: parsedExpected.value,
      ...(isOps ? { ops: value as TestCase['ops'] } : { input: value as TestCase['input'] }),
    })
    setName(''); setInput(''); setExpected(''); setError('')
  }

  return (
    <div className="space-y-2 text-sm">
      <div className="grid gap-2 sm:grid-cols-2">
        <Input className="h-8 sm:col-span-2" placeholder="Case name" value={name} onChange={(e) => setName(e.target.value)} />
        <Textarea
          className="font-mono text-xs"
          rows={3}
          placeholder={`${isOps ? 'Ops' : 'Input'} as JSON, e.g. ${JSON.stringify(template)}`}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <Textarea className="font-mono text-xs" rows={3} placeholder="Expected as JSON" value={expected} onChange={(e) => setExpected(e.target.value)} />
      </div>
      <div className="flex items-center gap-2">
        <Button size="sm" onClick={save}>Add case</Button>
        {error && <span className="text-xs text-destructive">{error}</span>}
      </div>
      {cases.length > 0 && (
        <ul className="divide-y rounded-md border">
          {cases.map((c) => (
            <li key={c.name} className="flex items-center justify-between gap-2 px-2 py-1">
              <span className="truncate">
                {c.name} <Badge variant="outline">custom</Badge>
                <span className="ml-2 font-mono text-xs text-muted-foreground">{JSON.stringify(c.input ?? c.ops)} → {JSON.stringify(c.expected)}</span>
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
