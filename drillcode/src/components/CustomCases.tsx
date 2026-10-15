import { Plus, Trash2 } from 'lucide-react'
import { useMemo, useState } from 'react'
import { ChevronDown, ChevronRight } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { skeletonSource } from '@/lib/catalogue'
import { caseHelp, formatCase, inputNames, parseCaseLine, parseJson, splitTopLevel } from '@/lib/caseFormat'
import { useStore } from '@/lib/store'
import { parseTyped, typeError } from '@/lib/valueTypes'
import type { TestCase, TestsSpec } from '@/lib/types'

const NONE: TestCase[] = []
const show = (v: unknown) => JSON.stringify(v)

/** `{ nums: 'List[int]', target: 'int' }` read from the skeleton's method signature, plus the return type under `->`. */
function parameterTypes(slug: string, entry: string): Record<string, string> {
  // Ignore comment lines (the commented node definitions contain a `def __init__`) and match the entry method by name.
  const code = skeletonSource(slug).split('\n').filter((line) => !line.trimStart().startsWith('#')).join('\n')
  const method = entry.includes('.') ? entry.split('.')[1] : '\\w+'
  const header = code.match(new RegExp(`def ${method}\\(self,?([\\s\\S]*?)\\)\\s*(?:->\\s*([^:]*))?:`))
  if (!header) return {}
  const types: Record<string, string> = {}
  for (const param of splitTopLevel(header[1], ',')) {
    const [name, type] = param.split(/:(.*)/s).map((x) => x?.trim())
    if (name && type) types[name] = type.replace(/^'|'$/g, '')
  }
  if (header[2]) types['->'] = header[2].trim().replace(/^'|'$/g, '')
  return types
}

/** Function problems: one labelled field per argument, then the expected result. Design problems: calls and results. */
export function CustomCases({ slug, spec, allowReference }: { slug: string; spec: TestsSpec; allowReference: boolean }) {
  const cases = useStore((s) => s.customCases[slug]) ?? NONE
  const { addCustomCase, removeCustomCase } = useStore()
  const names = useMemo(() => inputNames(spec), [spec])
  const types = useMemo(() => parameterTypes(slug, spec.entry), [slug, spec.entry])
  const isOps = spec.kind === 'operations'
  const example = spec.cases[0]

  const [values, setValues] = useState<Record<string, string>>({})
  const [calls, setCalls] = useState('')
  const [expected, setExpected] = useState('')
  const [expectedOpen, setExpectedOpen] = useState(false)

  const inPlace = spec.compare?.startsWith('in_place:') ? spec.compare.split(':')[1] : null

  // Parse every filled field; the form can be added only when all of them parse.
  const fields = names.map((name) => {
    const text = values[name] ?? ''
    const parsed = text.trim() ? parseTyped(text, types[name], name) : null
    const mismatch = parsed && !parsed.error ? typeError(parsed.value, types[name]) : null
    return { name, text, parsed, mismatch }
  })
  const expectedParsed = expected.trim() ? parseJson(expected, 'the expected result') : null
  // Blank expected on a design problem: parse the calls against placeholder nulls, then drop them.
  const blankExpected = !expected.trim()
  const placeholder = JSON.stringify(Array(splitTopLevel(calls, ';').length).fill(null))
  const opsParsed = isOps && calls.trim() ? parseCaseLine(spec, `${calls} → ${blankExpected ? placeholder : expected.trim()}`) : null

  // A blank expected value is fine when the reference solution can supply it.
  const expectedOk = blankExpected ? allowReference : !!expectedParsed && !expectedParsed.error
  const ready = isOps
    ? !!opsParsed?.case && expectedOk
    : fields.every((f) => f.parsed && !f.parsed.error && !f.mismatch) && expectedOk

  function add() {
    if (!ready) return
    const used = new Set(cases.map((c) => c.name))
    let n = cases.length + 1
    while (used.has(`my case ${n}`)) n++
    const name = `my case ${n}`
    if (isOps) {
      const parsedCase = { ...opsParsed!.case! }
      if (blankExpected) delete parsedCase.expected
      addCustomCase(slug, { name, ...parsedCase })
      setCalls('')
    } else {
      const input = Object.fromEntries(fields.map((f) => [f.name, f.parsed!.value]))
      addCustomCase(slug, { name, input, ...(blankExpected ? {} : { expected: expectedParsed!.value }), custom: true })
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
                className={`font-mono text-xs ${f.parsed?.error || f.mismatch ? 'border-destructive' : ''}`}
                spellCheck={false}
                value={f.text}
                onChange={(e) => setValues({ ...values, [f.name]: e.target.value })}
                onKeyDown={onEnter}
                placeholder={typeof example.input?.[f.name] === 'string' ? (example.input?.[f.name] as string) : show(example.input?.[f.name])}
              />
              {f.parsed?.error && <p className="text-xs text-destructive">Not a valid value. Use JSON, e.g. {show(example.input?.[f.name])}</p>}
              {f.mismatch && <p className="text-xs text-destructive"><span className="font-mono">{f.name}</span> {f.mismatch}.</p>}
            </div>
          ))
        )}
        {(() => {
          // The type of the expected value: the return type, the in-place argument, or a list for design problems.
          const type = isOps ? 'list' : inPlace ? types[inPlace] : types['->']
          const field = (
            <div className="space-y-1">
              <Input
                id="cc-expected"
                className={`font-mono text-xs ${expectedParsed?.error ? 'border-destructive' : ''}`}
                spellCheck={false}
                value={expected}
                onChange={(e) => setExpected(e.target.value)}
                onKeyDown={onEnter}
                placeholder={show(example.expected)}
                aria-label="expected"
              />
              {expectedParsed?.error && <p className="text-xs text-destructive">Not a valid value. Use JSON, e.g. {show(example.expected)}</p>}
            </div>
          )
          const typeText = type && <span className="font-mono font-normal text-muted-foreground">{type}</span>
          if (!allowReference) {
            // Required here (practice, or the answer is not the return value): always visible.
            return (
              <div className="space-y-1">
                <Label htmlFor="cc-expected" className="gap-1.5 text-xs"><span className="font-mono font-medium">expected</span>{typeText}</Label>
                {field}
              </div>
            )
          }
          return (
            <Collapsible open={expectedOpen} onOpenChange={setExpectedOpen} className="space-y-1">
              <CollapsibleTrigger className="flex items-center gap-1.5 text-xs">
                {expectedOpen ? <ChevronDown className="size-3.5" /> : <ChevronRight className="size-3.5" />}
                <span className="font-mono font-medium">expected</span>
                {typeText}
                <span className="font-normal text-muted-foreground">optional</span>
                {!expectedOpen && expected.trim() && <Badge variant="secondary" className="px-1.5 py-0 text-[10px]">set</Badge>}
              </CollapsibleTrigger>
              <CollapsibleContent>{field}</CollapsibleContent>
            </Collapsible>
          )
        })()}
      </div>
      <Button size="sm" onClick={add} disabled={!ready}>
        <Plus /> Add case
      </Button>

      {cases.length > 0 && (
        <ul className="divide-y rounded-md border">
          {[...cases].reverse().map((c) => (
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
