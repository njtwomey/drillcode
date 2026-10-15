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
  setTheme: (theme: Theme) => void
  setPracticeConfig: (patch: Partial<PracticeConfig>) => void
  startPractice: (slugs: string[]) => void
  practiceAttempt: (slug: string, passed: boolean) => void
  practiceAdvance: (skip: boolean) => void
  finishPractice: () => void
  discardPractice: () => void
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
      solves: [],
      toggleDone: (slug) =>
        set((s) => {
          const done = { ...s.done }
          if (done[slug]) delete done[slug]
          else done[slug] = true
          return { done }
        }),
      markDone: (slug) => set((s) => (s.done[slug] ? s : { done: { ...s.done, [slug]: true } })),
      resetProgress: () => set({ done: {}, practiceHistory: [], practice: null, solves: [] }),
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
      setTheme: (theme) => set({ theme }),
      setPracticeConfig: (patch) => set((s) => ({ practiceConfig: { ...s.practiceConfig, ...patch } })),
      startPractice: (slugs) =>
        set((s) => {
          const drafts = { ...s.drafts }
          for (const slug of slugs) delete drafts[practiceDraftKey(slug)]
          const now = Date.now()
          return {
            drafts,
            practice: {
              slugs, index: 0, startedAt: now, problemStartedAt: now, finished: false,
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
