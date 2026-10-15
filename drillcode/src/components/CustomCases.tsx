import { Plus, Trash2 } from 'lucide-react'
import { useMemo, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { skeletonSource } from '@/lib/catalogue'
import { caseHelp, formatCase, inputNames, parseCaseLine, parseJson, splitTopLevel } from '@/lib/caseFormat'
import { useStore } from '@/lib/store'
import type { TestCase, TestsSpec } from '@/lib/types'

const NONE: TestCase[] = []
const show = (v: unknown) => JSON.stringify(v)

/** `{ nums: 'List[int]', target: 'int' }` read from the skeleton's method signature. */
function parameterTypes(slug: string): Record<string, string> {
  const header = skeletonSource(slug).match(/def \w+\(self,?([\s\S]*?)\)\s*(?:->[^:]*)?:/)
  if (!header) return {}
  const types: Record<string, string> = {}
  for (const param of splitTopLevel(header[1], ',')) {
    const [name, type] = param.split(/:(.*)/s).map((x) => x?.trim())
    if (name && type) types[name] = type.replace(/^'|'$/g, '')
  }
  return types
}

/** Function problems: one labelled field per argument, then the expected result. Design problems: calls and results. */
export function CustomCases({ slug, spec }: { slug: string; spec: TestsSpec }) {
  const cases = useStore((s) => s.customCases[slug]) ?? NONE
  const { addCustomCase, removeCustomCase } = useStore()
  const names = useMemo(() => inputNames(spec), [spec])
  const types = useMemo(() => parameterTypes(slug), [slug])
  const isOps = spec.kind === 'operations'
  const example = spec.cases[0]

  const [values, setValues] = useState<Record<string, string>>({})
  const [calls, setCalls] = useState('')
  const [expected, setExpected] = useState('')

  const inPlace = spec.compare?.startsWith('in_place:') ? spec.compare.split(':')[1] : null

  // Parse every filled field; the form can be added only when all of them parse.
  const fields = names.map((name) => {
    const text = values[name] ?? ''
    return { name, text, parsed: text.trim() ? parseJson(`[${text}]`, name, text) : null }
  })
  const expectedParsed = expected.trim() ? parseJson(expected, 'the expected result') : null
  const opsParsed = isOps && calls.trim() ? parseCaseLine(spec, `${calls} → ${expected.trim() || 'null'}`) : null

  const ready = isOps
    ? !!opsParsed?.case && !!expected.trim()
    : fields.every((f) => f.parsed && !f.parsed.error) && !!expectedParsed && !expectedParsed.error

  function add() {
    if (!ready) return
    const used = new Set(cases.map((c) => c.name))
    let n = cases.length + 1
    while (used.has(`my case ${n}`)) n++
    const name = `my case ${n}`
    if (isOps) {
      addCustomCase(slug, { name, ...opsParsed!.case! })
      setCalls('')
    } else {
      const input = Object.fromEntries(fields.map((f) => [f.name, (f.parsed!.value as unknown[])[0]]))
      addCustomCase(slug, { name, input, expected: expectedParsed!.value, custom: true })
      setValues({})
    }
    setExpected('')
  }

  const onEnter = (e: React.KeyboardEvent) => e.key === 'Enter' && add()

  return (
    <div className="space-y-3 text-sm">
      <h3 className="font-medium">Add your own test case</h3>
      <div className="space-y-2.5">
        {isOps ? (
          <div className="space-y-1">
            <Label htmlFor="cc-calls" className="font-mono text-xs">calls</Label>
            <Input
              id="cc-calls" className="font-mono text-xs" spellCheck={false} value={calls} onChange={(e) => setCalls(e.target.value)}
              onKeyDown={onEnter} placeholder={example.ops!.map(([n, a]) => `${n}(${a.map(show).join(', ')})`).join('; ')}
            />
            <p className="text-xs text-muted-foreground">{caseHelp(spec)}</p>
            {opsParsed?.error && <p className="text-xs text-destructive">{opsParsed.error.replace(/^.*(?=Could not|The first|Expected)/, '')}</p>}
          </div>
        ) : (
          fields.map((f) => (
            <div key={f.name} className="space-y-1">
              <Label htmlFor={`cc-${f.name}`} className="gap-1.5 text-xs">
                <span className="font-mono font-medium">{f.name}</span>
                {types[f.name] && <span className="font-mono font-normal text-muted-foreground">{types[f.name]}</span>}
                {!(spec.args ?? []).includes(f.name) && (
                  <span className="font-normal text-muted-foreground">
                    {spec.extra_inputs?.[f.name] ?? 'used to build the input, not passed to your function'}
                  </span>
                )}
              </Label>
              <Input
                id={`cc-${f.name}`}
                className={`font-mono text-xs ${f.parsed?.error ? 'border-destructive' : ''}`}
                spellCheck={false}
                value={f.text}
                onChange={(e) => setValues({ ...values, [f.name]: e.target.value })}
                onKeyDown={onEnter}
                placeholder={show(example.input?.[f.name])}
              />
              {f.parsed?.error && <p className="text-xs text-destructive">Not a valid value. Use JSON, e.g. {show(example.input?.[f.name])}</p>}
            </div>
          ))
        )}
        <div className="space-y-1">
          <Label htmlFor="cc-expected" className="gap-1.5 text-xs">
            <span className="font-mono font-medium">expected</span>
            <span className="font-normal text-muted-foreground">
              {isOps ? 'one result per call, null for no result' : inPlace ? `the final ${inPlace}` : 'the return value'}
            </span>
          </Label>
          <Input
            id="cc-expected"
            className={`font-mono text-xs ${expectedParsed?.error ? 'border-destructive' : ''}`}
            spellCheck={false}
            value={expected}
            onChange={(e) => setExpected(e.target.value)}
            onKeyDown={onEnter}
            placeholder={show(example.expected)}
          />
          {expectedParsed?.error && <p className="text-xs text-destructive">Not a valid value. Use JSON, e.g. {show(example.expected)}</p>}
        </div>
      </div>
      <Button size="sm" onClick={add} disabled={!ready}>
        <Plus /> Add case
      </Button>

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
