import type { Difficulty, Problem } from './types'

export interface ProblemFilter {
  difficulties: Difficulty[]
  topics: string[]
  blind75Only: boolean
  search?: string
}

/** Topic filters match the primary topic or any tag. Search words must all match title, number, topic or tags. */
export function matchesFilter(p: Problem, f: ProblemFilter): boolean {
  if (f.difficulties.length && !f.difficulties.includes(p.difficulty)) return false
  if (f.topics.length && !f.topics.some((t) => t === p.topic || p.tags.includes(t))) return false
  if (f.blind75Only && !p.blind75) return false
  const words = (f.search ?? '').toLowerCase().split(/\s+/).filter(Boolean)
  if (words.length) {
    const haystack = `${p.number} ${p.title} ${p.topic} ${p.tags.join(' ')}`.toLowerCase()
    if (!words.every((w) => haystack.includes(w))) return false
  }
  return true
}
