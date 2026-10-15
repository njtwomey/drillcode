import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Difficulty, Mode, TestCase } from './types'

/** Which problems to include: everything, only those not done yet, or only those already done (for review). */
export type StatusFilter = 'all' | 'todo' | 'done'

export interface Filters {
  difficulties: Difficulty[]
  topics: string[]
  blind75Only: boolean
  status: StatusFilter
  search: string
}

export type SortKey = 'done' | 'solves' | 'number' | 'title' | 'difficulty' | 'topic' | 'tags' | 'flags'
export interface Sort {
  key: SortKey | null
  dir: 'asc' | 'desc'
}

export interface PracticeConfig {
  difficulties: Difficulty[]
  topics: string[]
  blind75Only: boolean
  status: StatusFilter
  count: number
}

export interface PracticeOutcome {
  status: 'pending' | 'passed' | 'skipped'
  attempts: number
  seconds: number
}

export interface PracticeSession {
  slugs: string[]
  /** Time-based seed the problems were shuffled with. */
  seed?: number
  index: number
  startedAt: number
  problemStartedAt: number
  outcomes: Record<string, PracticeOutcome>
  finished: boolean
}

/** One time a problem was solved: every test passed in Practice, or in Implement mode. */
export interface SolveEvent {
  slug: string
  at: number
  source: 'practice' | 'implement'
  seconds?: number
}

/** Criteria for the random walk: the session filters without a count. */
export type WalkConfig = Omit<PracticeConfig, 'count'>

/** A random walk: no count and no end; it keeps its place until you end it. */
export interface WalkState {
  /** Problems visited, in order; `index` is the one on screen (Back and Forward move along this list). */
  history: string[]
  index: number
  outcomes: Record<string, PracticeOutcome>
  problemStartedAt: number
  startedAt: number
}

export interface PracticeRecord {
  finishedAt: number
  total: number
  passed: number
  seconds: number
}

export type Theme = 'light' | 'dark'

interface State {
  done: Record<string, true>
  filters: Filters
  sort: Sort
  drafts: Record<string, string>
  customCases: Record<string, TestCase[]>
  theme: Theme
  practiceConfig: PracticeConfig
  practice: PracticeSession | null
  practiceHistory: PracticeRecord[]
  walkConfig: WalkConfig
  walk: WalkState | null
  solves: SolveEvent[]
  toggleDone: (slug: string) => void
  markDone: (slug: string) => void
  resetProgress: () => void
  recordSolve: (event: Omit<SolveEvent, 'at'>) => void
  setFilters: (patch: Partial<Filters>) => void
  clearFilters: () => void
  setSort: (sort: Sort) => void
  setDraft: (key: string, source: string) => void
  clearDraft: (key: string) => void
  addCustomCase: (slug: string, testCase: TestCase) => void
  removeCustomCase: (slug: string, name: string) => void
  updateCustomCase: (slug: string, name: string, patch: Partial<TestCase>) => void
  setTheme: (theme: Theme) => void
  setPracticeConfig: (patch: Partial<PracticeConfig>) => void
  startPractice: (slugs: string[], seed?: number) => void
  practiceAttempt: (slug: string, passed: boolean) => void
  practiceAdvance: (skip: boolean) => void
  finishPractice: () => void
  discardPractice: () => void
  setWalkConfig: (patch: Partial<WalkConfig>) => void
  startWalk: (slug: string) => void
  walkGo: (slug: string) => void
  walkMove: (delta: -1 | 1) => void
  walkAttempt: (slug: string, passed: boolean) => void
  endWalk: () => void
}

/** Draft slot: one per slug and mode; View mode has one more per alternative solution. */
export const draftKey = (slug: string, mode: Mode, variant = 'primary') =>
  mode === 'view' && variant !== 'primary' ? `${slug}:view:${variant}` : `${slug}:${mode}`
export const practiceDraftKey = (slug: string) => `practice:${slug}`

const DEFAULT_FILTERS: Filters = { difficulties: [], topics: [], blind75Only: false, status: 'all', search: '' }

function finished(session: PracticeSession): { session: PracticeSession; record: PracticeRecord } {
  const outcomes = Object.values(session.outcomes)
  return {
    session: { ...session, finished: true },
    record: {
      finishedAt: Date.now(),
      total: session.slugs.length,
      passed: outcomes.filter((o) => o.status === 'passed').length,
      seconds: outcomes.reduce((sum, o) => sum + o.seconds, 0),
    },
  }
}

export const useStore = create<State>()(
  persist(
    (set) => ({
      done: {},
      filters: DEFAULT_FILTERS,
      sort: { key: null, dir: 'asc' },
      drafts: {},
      customCases: {},
      theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
      practiceConfig: { difficulties: [], topics: [], blind75Only: false, status: 'todo', count: 5 },
      practice: null,
      practiceHistory: [],
      walkConfig: { difficulties: [], topics: [], blind75Only: false, status: 'todo' },
      walk: null,
      solves: [],
      toggleDone: (slug) =>
        set((s) => {
          const done = { ...s.done }
          if (done[slug]) delete done[slug]
          else done[slug] = true
          return { done }
        }),
      markDone: (slug) => set((s) => (s.done[slug] ? s : { done: { ...s.done, [slug]: true } })),
      resetProgress: () => set({ done: {}, practiceHistory: [], practice: null, walk: null, solves: [] }),
      recordSolve: (event) => set((s) => ({ solves: [...s.solves, { ...event, at: Date.now() }].slice(-5000) })),
      setFilters: (patch) => set((s) => ({ filters: { ...s.filters, ...patch } })),
      clearFilters: () => set({ filters: DEFAULT_FILTERS }),
      setSort: (sort) => set({ sort }),
      setDraft: (key, source) => set((s) => ({ drafts: { ...s.drafts, [key]: source } })),
      clearDraft: (key) =>
        set((s) => {
          const drafts = { ...s.drafts }
          delete drafts[key]
          return { drafts }
        }),
      addCustomCase: (slug, testCase) =>
        set((s) => ({
          customCases: {
            ...s.customCases,
            [slug]: [...(s.customCases[slug] ?? []).filter((c) => c.name !== testCase.name), testCase],
          },
        })),
      removeCustomCase: (slug, name) =>
        set((s) => ({
          customCases: { ...s.customCases, [slug]: (s.customCases[slug] ?? []).filter((c) => c.name !== name) },
        })),
      updateCustomCase: (slug, name, patch) =>
        set((s) => ({
          customCases: { ...s.customCases, [slug]: (s.customCases[slug] ?? []).map((c) => (c.name === name ? { ...c, ...patch } : c)) },
        })),
      setTheme: (theme) => set({ theme }),
      setPracticeConfig: (patch) => set((s) => ({ practiceConfig: { ...s.practiceConfig, ...patch } })),
      startPractice: (slugs, seed) =>
        set((s) => {
          const drafts = { ...s.drafts }
          for (const slug of slugs) delete drafts[practiceDraftKey(slug)]
          const now = Date.now()
          return {
            drafts,
            practice: {
              slugs, seed, index: 0, startedAt: now, problemStartedAt: now, finished: false,
              outcomes: Object.fromEntries(slugs.map((slug) => [slug, { status: 'pending', attempts: 0, seconds: 0 }])),
            },
          }
        }),
      practiceAttempt: (slug, passed) =>
        set((s) => {
          if (!s.practice) return {}
          const current = s.practice.outcomes[slug]
          const seconds = passed && current.status !== 'passed'
            ? Math.round((Date.now() - s.practice.problemStartedAt) / 1000)
            : current.seconds
          const status = passed ? 'passed' : current.status
          return {
            practice: {
              ...s.practice,
              outcomes: { ...s.practice.outcomes, [slug]: { status, attempts: current.attempts + 1, seconds } },
            },
          }
        }),
      practiceAdvance: (skip) =>
        set((s) => {
          const p = s.practice
          if (!p) return {}
          const slug = p.slugs[p.index]
          const current = p.outcomes[slug]
          const outcomes = {
            ...p.outcomes,
            [slug]: current.status === 'pending' && skip ? { ...current, status: 'skipped' as const } : current,
          }
          const next = { ...p, outcomes, index: p.index + 1, problemStartedAt: Date.now() }
          if (next.index >= p.slugs.length) {
            const { session, record } = finished({ ...next, index: p.slugs.length - 1 })
            return { practice: session, practiceHistory: [record, ...s.practiceHistory].slice(0, 50) }
          }
          return { practice: next }
        }),
      finishPractice: () =>
        set((s) => {
          if (!s.practice) return {}
          const { session, record } = finished(s.practice)
          return { practice: session, practiceHistory: [record, ...s.practiceHistory].slice(0, 50) }
        }),
      discardPractice: () => set({ practice: null }),
      setWalkConfig: (patch) => set((s) => ({ walkConfig: { ...s.walkConfig, ...patch } })),
      // A newly reached problem always starts from a blank skeleton; going Back keeps your code.
      startWalk: (slug) =>
        set((s) => {
          const drafts = { ...s.drafts }
          delete drafts[practiceDraftKey(slug)]
          const now = Date.now()
          return {
            drafts,
            walk: { history: [slug], index: 0, startedAt: now, problemStartedAt: now, outcomes: { [slug]: { status: 'pending', attempts: 0, seconds: 0 } } },
          }
        }),
      walkGo: (slug) =>
        set((s) => {
          if (!s.walk) return {}
          const drafts = { ...s.drafts }
          delete drafts[practiceDraftKey(slug)]
          const outcomes = { ...s.walk.outcomes }
          const current = s.walk.history[s.walk.index]
          if (outcomes[current]?.status === 'pending') outcomes[current] = { ...outcomes[current], status: 'skipped' }
          outcomes[slug] = { status: 'pending', attempts: 0, seconds: 0 }
          const history = [...s.walk.history.slice(0, s.walk.index + 1), slug]
          return { drafts, walk: { ...s.walk, history, index: history.length - 1, outcomes, problemStartedAt: Date.now() } }
        }),
      walkMove: (delta) =>
        set((s) => {
          if (!s.walk) return {}
          const index = Math.min(Math.max(s.walk.index + delta, 0), s.walk.history.length - 1)
          return { walk: { ...s.walk, index, problemStartedAt: Date.now() } }
        }),
      walkAttempt: (slug, passed) =>
        set((s) => {
          if (!s.walk) return {}
          const current = s.walk.outcomes[slug] ?? { status: 'pending' as const, attempts: 0, seconds: 0 }
          const seconds = passed && current.status !== 'passed' ? Math.round((Date.now() - s.walk.problemStartedAt) / 1000) : current.seconds
          return {
            walk: {
              ...s.walk,
              outcomes: { ...s.walk.outcomes, [slug]: { status: passed ? 'passed' : current.status, attempts: current.attempts + 1, seconds } },
            },
          }
        }),
      endWalk: () => set({ walk: null }),
    }),
    {
      name: 'leetcode-workbench',
      version: 2,
      // v1 had `hideDone` / `skipDone` switches and a shuffle queue; v2 has a three-way status filter.
      migrate: (persisted) => {
        const old = persisted as Record<string, any> // eslint-disable-line @typescript-eslint/no-explicit-any
        const { queue: _queue, queuePos: _pos, ...rest } = old // eslint-disable-line @typescript-eslint/no-unused-vars
        const filters = { ...DEFAULT_FILTERS, ...old.filters }
        filters.status = old.filters?.hideDone ? 'todo' : (old.filters?.status ?? 'all')
        delete (filters as Record<string, unknown>).hideDone
        const config = { ...old.practiceConfig }
        config.status = old.practiceConfig?.skipDone === false ? 'all' : (old.practiceConfig?.status ?? 'todo')
        delete config.skipDone
        return { ...rest, filters, practiceConfig: { difficulties: [], topics: [], blind75Only: false, count: 5, ...config } } as unknown as State
      },
    },
  ),
)
