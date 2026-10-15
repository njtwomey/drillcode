import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Difficulty, Mode, TestCase } from './types'

export interface Filters {
  difficulties: Difficulty[]
  topics: string[]
  blind75Only: boolean
  hideDone: boolean
  search: string
}

export type Theme = 'light' | 'dark'

interface State {
  done: Record<string, true>
  filters: Filters
  queue: string[]
  queuePos: number
  drafts: Record<string, string>
  customCases: Record<string, TestCase[]>
  theme: Theme
  toggleDone: (slug: string) => void
  setFilters: (patch: Partial<Filters>) => void
  setQueue: (queue: string[]) => void
  setQueuePos: (pos: number) => void
  clearQueue: () => void
  setDraft: (key: string, source: string) => void
  clearDraft: (key: string) => void
  addCustomCase: (slug: string, testCase: TestCase) => void
  removeCustomCase: (slug: string, name: string) => void
  setTheme: (theme: Theme) => void
}

/** Draft slot: one per slug and mode; View mode has one more per alternative solution. */
export const draftKey = (slug: string, mode: Mode, variant = 'primary') =>
  mode === 'view' && variant !== 'primary' ? `${slug}:view:${variant}` : `${slug}:${mode}`

export const useStore = create<State>()(
  persist(
    (set) => ({
      done: {},
      filters: { difficulties: [], topics: [], blind75Only: false, hideDone: false, search: '' },
      queue: [],
      queuePos: 0,
      drafts: {},
      customCases: {},
      theme: window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light',
      toggleDone: (slug) =>
        set((s) => {
          const done = { ...s.done }
          if (done[slug]) delete done[slug]
          else done[slug] = true
          return { done }
        }),
      setFilters: (patch) => set((s) => ({ filters: { ...s.filters, ...patch } })),
      setQueue: (queue) => set({ queue, queuePos: 0 }),
      setQueuePos: (queuePos) => set({ queuePos }),
      clearQueue: () => set({ queue: [], queuePos: 0 }),
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
    }),
    { name: 'leetcode-workbench' },
  ),
)
