import type { SolveEvent } from './store'

export interface SolveStats {
  count: number
  last: number
  bestSeconds?: number
}

/** Per-problem totals from the solve log. */
export function solveStats(solves: SolveEvent[]): Map<string, SolveStats> {
  const stats = new Map<string, SolveStats>()
  for (const e of solves) {
    const current = stats.get(e.slug) ?? { count: 0, last: 0 }
    current.count += 1
    current.last = Math.max(current.last, e.at)
    if (e.seconds !== undefined) current.bestSeconds = Math.min(current.bestSeconds ?? Infinity, e.seconds)
    stats.set(e.slug, current)
  }
  return stats
}

const DAY = 24 * 60 * 60 * 1000

/** "today", "yesterday", "3 days ago", "2 weeks ago", "5 months ago". */
export function formatAgo(timestamp: number, now = Date.now()): string {
  const days = Math.floor((startOfDay(now) - startOfDay(timestamp)) / DAY)
  if (days <= 0) return 'today'
  if (days === 1) return 'yesterday'
  if (days < 14) return `${days} days ago`
  if (days < 60) return `${Math.floor(days / 7)} weeks ago`
  return `${Math.floor(days / 30)} months ago`
}

function startOfDay(timestamp: number): number {
  const d = new Date(timestamp)
  return new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime()
}

/** Consecutive days, ending today or yesterday, with at least one solve. */
export function currentStreak(solves: SolveEvent[], now = Date.now()): number {
  const days = new Set(solves.map((e) => startOfDay(e.at)))
  let day = startOfDay(now)
  if (!days.has(day)) day -= DAY
  let streak = 0
  while (days.has(day)) {
    streak += 1
    day -= DAY
  }
  return streak
}
