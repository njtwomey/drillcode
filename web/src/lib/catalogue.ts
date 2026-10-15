import { parse } from 'yaml'
import type { Problem, TestsSpec } from './types'
import indexRaw from '../../../problems/index.yaml?raw'

// Everything under problems/ is read straight from disk, so edits hot-reload.
const problemFiles = import.meta.glob(
  '../../../problems/*/{solution*.py,skeleton.py,tests.yaml,validator.py,description.md}',
  { query: '?raw', import: 'default', eager: true },
) as Record<string, string>

const scaffoldFiles = import.meta.glob('../../../problems/_scaffolds/*.py', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

const harnessFiles = import.meta.glob('../../../problems/_harness/runner.py', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>

export const problems: Problem[] = parse(indexRaw)
export const bySlug = new Map(problems.map((p) => [p.slug, p]))

export const TOPICS = [
  'Array', 'String', 'Hash', 'Two pointers', 'Sliding window', 'Stack', 'Monotonic stack',
  'Binary search', 'Linked list', 'Tree', 'Trie', 'Heap', 'Graph', 'Intervals', 'Matrix',
  'DP', 'Greedy', 'Backtracking', 'Bit manipulation', 'Design',
]

function file(slug: string, name: string): string | undefined {
  return problemFiles[`../../../problems/${slug}/${name}`]
}

export function hasFiles(slug: string): boolean {
  return file(slug, 'tests.yaml') !== undefined
}

export function solutionSource(slug: string) {
  return file(slug, 'solution.py') ?? ''
}
export interface Variant {
  id: string // 'primary' or the solution_<id>.py suffix
  label: string
  source: string
}

/** solution.py first, then any solution_<variant>.py alternatives (same tests, different approach). */
export function solutionVariants(slug: string): Variant[] {
  const prefix = `../../../problems/${slug}/`
  const variants: Variant[] = [{ id: 'primary', label: 'Primary', source: solutionSource(slug) }]
  for (const path of Object.keys(problemFiles).sort()) {
    const match = path.startsWith(prefix) && path.slice(prefix.length).match(/^solution_(.+)\.py$/)
    if (match) variants.push({ id: match[1], label: match[1].replace(/_/g, ' '), source: problemFiles[path] })
  }
  return variants
}

export function skeletonSource(slug: string) {
  return file(slug, 'skeleton.py') ?? ''
}
export function descriptionSource(slug: string): string | undefined {
  return file(slug, 'description.md')
}
export function validatorSource(slug: string) {
  return file(slug, 'validator.py')
}

const specCache = new Map<string, TestsSpec>()
export function testsSpec(slug: string): TestsSpec | undefined {
  const cached = specCache.get(slug)
  if (cached) return cached
  const raw = file(slug, 'tests.yaml')
  if (raw === undefined) return undefined
  const spec = parse(raw) as TestsSpec
  specCache.set(slug, spec)
  return spec
}

/** The commented class definitions at the top of skeleton.py. */
export function definitions(slug: string): string {
  const lines: string[] = []
  for (const line of skeletonSource(slug).split('\n')) {
    if (!line.startsWith('#')) break
    lines.push(line)
  }
  return lines.join('\n')
}

/** Files the worker writes into the Pyodide filesystem: scaffolds and the harness. */
export function pythonSupportFiles(): Record<string, string> {
  const files: Record<string, string> = {}
  for (const [path, source] of [...Object.entries(scaffoldFiles), ...Object.entries(harnessFiles)]) {
    files[path.split('/').pop()!] = source
  }
  return files
}

export function reloadSpecCache() {
  specCache.clear()
}
if (import.meta.hot) import.meta.hot.on('vite:beforeUpdate', reloadSpecCache)
