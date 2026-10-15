export type Difficulty = 'easy' | 'medium' | 'hard'
export type Mode = 'view' | 'implement'

export interface Problem {
  slug: string
  number: number
  title: string
  difficulty: Difficulty
  topic: string
  tags: string[]
  blind75: boolean
  premium: boolean
  leetcode: string
  summary: string
  tricks: string
  edge_cases: string[]
  complexity: { time: string; space: string }
}

export interface TestCase {
  name: string
  input?: Record<string, unknown>
  ops?: [string, unknown[]][]
  expected: unknown
  custom?: boolean
}

export interface TestsSpec {
  kind: 'function' | 'operations'
  entry: string
  scaffolds: string[]
  args?: string[]
  convert?: Record<string, string>
  compare?: string
  call?: boolean
  cases: TestCase[]
}

export type CaseStatus = 'pass' | 'fail' | 'error' | 'timeout' | 'skipped'

export interface CaseResult {
  name: string
  status: CaseStatus
  ms: number
  expected: unknown
  actual: unknown
  message: string
  stdout: string
  stderr: string
  custom?: boolean
}

export type PyStatus = 'loading' | 'ready' | 'running' | 'restarting' | 'error'
