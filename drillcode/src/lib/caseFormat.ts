import type { TestCase, TestsSpec } from './types'

const ARROW = /->|=>|→/g

/** Names of the values a case line holds, in order: the call arguments, then converter extras (e.g. `pos`). */
export function inputNames(spec: TestsSpec): string[] {
  const names = [...(spec.args ?? [])]
  for (const conv of Object.values(spec.convert ?? {})) {
    const extra = conv.includes(':') ? conv.split(':')[1] : undefined
    if (extra && !names.includes(extra) && !(conv.startsWith('tree_node:'))) names.push(extra)
  }
  return names
}

const show = (v: unknown) => JSON.stringify(v)

/** One readable line: `[2,7,11,15], 9 → [0,1]` or `LRUCache(2); put(1, 1); get(1) → [null,null,1]`. */
export function formatCase(spec: TestsSpec, c: TestCase): string {
  if (spec.kind === 'operations') {
    const calls = (c.ops ?? []).map(([name, args]) => `${name}(${args.map(show).join(', ')})`)
    return `${calls.join('; ')} → ${show(c.expected)}`
  }
  const values = inputNames(spec).map((n) => show(c.input?.[n]))
  return `${values.join(', ')} → ${show(c.expected)}`
}

/** Python-ish literals to JSON: True/False/None, single-quoted strings, trailing commas left alone. */
export function pythonToJson(text: string): string {
  let out = ''
  for (let i = 0; i < text.length; i++) {
    const ch = text[i]
    if (ch === '"' || ch === "'") {
      let j = i + 1
      let body = ''
      while (j < text.length && text[j] !== ch) {
        if (text[j] === '\\' && j + 1 < text.length) body += text[j++]
        body += text[j++]
      }
      if (j >= text.length) return text // unterminated: let JSON.parse report it
      out += ch === '"' ? `"${body}"` : `"${body.replace(/"/g, '\\"')}"`
      i = j
    } else if (/[A-Za-z_]/.test(ch)) {
      let j = i
      while (j < text.length && /\w/.test(text[j])) j++
      const word = text.slice(i, j)
      out += word === 'True' ? 'true' : word === 'False' ? 'false' : word === 'None' ? 'null' : word
      i = j - 1
    } else out += ch
  }
  return out
}

export function parseJson(text: string, what: string, shown = text): { value?: unknown; error?: string } {
  try {
    return { value: JSON.parse(pythonToJson(text)) }
  } catch {
    return { error: `Could not read ${what}: ${shown.trim() || '(empty)'}` }
  }
}

/** Split on a separator that is not inside brackets or a string. */
export function splitTopLevel(text: string, sep: string): string[] {
  const parts: string[] = []
  let depth = 0
  let quote = ''
  let start = 0
  for (let i = 0; i < text.length; i++) {
    const ch = text[i]
    if (quote) {
      if (ch === '\\') i++
      else if (ch === quote) quote = ''
    } else if (ch === '"' || ch === "'") quote = ch
    else if ('([{'.includes(ch)) depth++
    else if (')]}'.includes(ch)) depth--
    else if (ch === sep && depth === 0) {
      parts.push(text.slice(start, i))
      start = i + 1
    }
  }
  parts.push(text.slice(start))
  return parts.filter((p) => p.trim())
}

/** Hint shown under the field: how to write a case for this problem. */
export function caseHelp(spec: TestsSpec): string {
  if (spec.kind === 'operations') {
    const cls = spec.entry
    return `Calls separated by ";" then → the list of results. Start with the constructor, e.g. ${cls}(...); method(...) → [null, ...]`
  }
  return `Values in order (${inputNames(spec).join(', ')}) then → expected result.`
}

/** Parse `values → expected` (or `Class(..); call(..) → [..]`) into a test case. */
export function parseCaseLine(spec: TestsSpec, text: string): { case?: Omit<TestCase, 'name'>; error?: string } {
  const arrows = [...text.matchAll(ARROW)]
  if (!arrows.length) return { error: 'Write the input, then → (or ->), then the expected result.' }
  const at = arrows[arrows.length - 1]
  const left = text.slice(0, at.index)
  const right = text.slice(at.index + at[0].length)
  if (!left.trim()) return { error: 'Nothing before the arrow: write the input first.' }
  if (!right.trim()) return { error: 'Nothing after the arrow: write the expected result.' }
  const expected = parseJson(right, 'the expected result')
  if (expected.error) return { error: expected.error }

  if (spec.kind === 'operations') {
    const ops: [string, unknown[]][] = []
    for (const call of splitTopLevel(left, ';')) {
      const m = call.trim().match(/^([A-Za-z_]\w*)\s*\(([\s\S]*)\)$/)
      if (!m) return { error: `Could not read the call “${call.trim()}”. Use name(arg, arg).` }
      const args = parseJson(`[${m[2]}]`, `the arguments of ${m[1]}`, m[2])
      if (args.error) return { error: args.error }
      ops.push([m[1], args.value as unknown[]])
    }
    if (ops[0][0] !== spec.entry) return { error: `The first call must be the constructor ${spec.entry}(...).` }
    if (!Array.isArray(expected.value) || expected.value.length !== ops.length) {
      return { error: `Expected must be a list with one result per call (${ops.length}), use null for calls that return nothing.` }
    }
    return { case: { ops, expected: expected.value, custom: true } }
  }

  const values = parseJson(`[${left}]`, 'the input values', left)
  if (values.error) return { error: values.error }
  const names = inputNames(spec)
  const list = values.value as unknown[]
  if (list.length !== names.length) {
    return { error: `This problem takes ${names.length} value${names.length === 1 ? '' : 's'} (${names.join(', ')}) but you wrote ${list.length}.` }
  }
  const input = Object.fromEntries(names.map((n, i) => [n, list[i]]))
  return { case: { input, expected: expected.value, custom: true } }
}
