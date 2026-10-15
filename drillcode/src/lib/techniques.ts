import { parse } from 'yaml'
import { bySlug } from './catalogue'

// techniques/*.md are read straight from disk like the rest of problems/, so edits hot-reload.
const files = import.meta.glob('../../../techniques/*.md', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

export const AREAS = [
  'Linked lists', 'Pointers and windows', 'Hashing and counting', 'Stacks', 'Binary search', 'Trees',
  'Graphs', 'Backtracking', 'Heaps', 'Intervals', 'Dynamic programming', 'Greedy', 'Matrices', 'Bits',
  'Tries', 'Design',
] as const

export interface Section {
  heading: string
  body: string
}

export interface Technique {
  slug: string
  title: string
  area: string
  topics: string[]
  problems: string[]
  related: string[]
  body: string
  sections: Section[]
  /** First bullet of "Reach for it when". */
  signal: string
}

function splitFrontmatter(text: string): { meta: Record<string, unknown>; body: string } {
  const match = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/)
  if (!match) return { meta: {}, body: text }
  return { meta: (parse(match[1]) as Record<string, unknown>) ?? {}, body: match[2] }
}

/** Split on `## ` headings, ignoring lines inside code fences. */
function splitSections(body: string): Section[] {
  const sections: Section[] = []
  let inFence = false
  for (const line of body.split('\n')) {
    if (line.startsWith('```')) inFence = !inFence
    const heading = !inFence && line.match(/^##\s+(.*?)\s*$/)
    if (heading) sections.push({ heading: heading[1], body: '' })
    else if (sections.length) sections[sections.length - 1].body += `${line}\n`
  }
  return sections.map((s) => ({ ...s, body: s.body.trim() }))
}

const list = (v: unknown): string[] => (Array.isArray(v) ? (v as string[]) : [])

let signalsMarkdown = ''
const parsed: Technique[] = []
for (const [path, raw] of Object.entries(files)) {
  const name = path.split('/').pop()!.replace(/\.md$/, '')
  const { meta, body } = splitFrontmatter(raw)
  if (name === '_index') {
    signalsMarkdown = raw
    continue
  }
  const sections = splitSections(body)
  const reach = sections.find((s) => s.heading === 'Reach for it when')?.body ?? ''
  const first = reach.split('\n').find((l) => l.trim().startsWith('-')) ?? reach.split('\n')[0] ?? ''
  parsed.push({
    slug: name,
    title: String(meta.title ?? name),
    area: String(meta.area ?? ''),
    topics: list(meta.topics),
    problems: list(meta.problems),
    related: list(meta.related),
    body,
    sections,
    signal: first.replace(/^\s*-\s*/, ''),
  })
}

/** One row of the signals table in _index.md: a situation, and the techniques (as links) that answer it. */
export interface SignalRow {
  signal: string
  /** Alternating plain text and technique slugs, in reading order. */
  parts: ({ text: string } | { slug: string })[]
  slugs: string[]
}

function parseSignals(markdown: string): SignalRow[] {
  const rows: SignalRow[] = []
  for (const line of markdown.split('\n')) {
    if (!line.startsWith('|') || /^\|\s*-/.test(line) || /^\|\s*When the problem/i.test(line)) continue
    const cells = line.split('|').slice(1, -1).map((c) => c.trim())
    if (cells.length < 2) continue
    const parts: SignalRow['parts'] = []
    const slugs: string[] = []
    for (const piece of cells[1].split(/(`[^`]+`)/g)) {
      if (!piece) continue
      if (piece.startsWith('`')) {
        const slug = piece.slice(1, -1)
        parts.push({ slug })
        slugs.push(slug)
      } else parts.push({ text: piece })
    }
    rows.push({ signal: cells[0], parts, slugs })
  }
  return rows
}

const areaRank = (area: string) => {
  const i = (AREAS as readonly string[]).indexOf(area)
  return i === -1 ? AREAS.length : i
}
export const techniques: Technique[] = parsed.sort(
  (a, b) => areaRank(a.area) - areaRank(b.area) || a.title.localeCompare(b.title),
)
export const signalsTable = signalsMarkdown
export const signalRows: SignalRow[] = parseSignals(signalsMarkdown)

/** Everything a search should match for one technique: its text, its area and topics, the signal rows that point at it, and the problems it lists. */
export function searchText(t: Technique): string {
  const signals = signalRows.filter((r) => r.slugs.includes(t.slug)).map((r) => r.signal)
  const problems = t.problems.flatMap((slug) => {
    const p = bySlug.get(slug)
    return p ? [`${p.number} ${p.title} ${p.topic} ${p.tags.join(' ')} ${p.difficulty}`] : []
  })
  return [t.title, t.area, t.topics.join(' '), t.slug.replace(/-/g, ' '), t.body, ...signals, ...problems].join(' ').toLowerCase()
}
export const techniqueBySlug = new Map(techniques.map((t) => [t.slug, t]))

/** Reverse index: the techniques whose `problems` list contains this slug. */
export function techniquesForProblem(slug: string): Technique[] {
  return techniques.filter((t) => t.problems.includes(slug))
}
