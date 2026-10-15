import { parseJson } from './caseFormat'

const squash = (type?: string) => (type ?? '').replace(/\s+/g, '').replace(/^'|'$/g, '')

/**
 * Read what was typed into an input field. A `str` parameter takes the text as it is, no quotes needed
 * (write "..." only if you want the quotes handled as JSON); everything else is JSON or Python literals.
 */
export function parseTyped(text: string, type: string | undefined, what: string): { value?: unknown; error?: string } {
  if (squash(type) === 'str' && !/^\s*["']/.test(text)) return { value: text.trim() }
  const parsed = parseJson(`[${text}]`, what, text)
  return parsed.error ? { error: parsed.error } : { value: (parsed.value as unknown[])[0] }
}

const describe = (v: unknown) => (v === null ? 'null' : Array.isArray(v) ? 'a list' : typeof v === 'string' ? 'text' : typeof v === 'number' ? 'a number' : typeof v)

/** A plain-English problem with `value` against a simple Python type, or null when it fits or the type is not checked. */
export function typeError(value: unknown, type: string | undefined): string | null {
  const t = squash(type)
  if (!t) return null
  const optional = t.match(/^Optional\[(.*)\]$/)
  if (optional) return value === null ? null : typeError(value, optional[1])
  switch (t) {
    case 'int':
      if (Number.isInteger(value)) return null
      return typeof value === 'number' ? 'needs a whole number, but this has a decimal part' : `needs a whole number, but this is ${describe(value)}`
    case 'float': return typeof value === 'number' ? null : `needs a number, but this is ${describe(value)}`
    case 'bool': return typeof value === 'boolean' ? null : `needs true or false, but this is ${describe(value)}`
    case 'str': return typeof value === 'string' ? null : `needs text, but this is ${describe(value)}`
  }
  const list = t.match(/^List\[(.*)\]$/)
  if (list) {
    if (!Array.isArray(value)) return `needs a list like [...], but this is ${describe(value)}`
    for (const item of value) {
      const problem = typeError(item, list[1])
      if (problem) return `has an item that ${problem}${list[1] === 'str' ? ' (put text in quotes inside a list)' : ''}`
    }
  }
  return null // nodes, dicts and the like are built by converters or not checked
}
