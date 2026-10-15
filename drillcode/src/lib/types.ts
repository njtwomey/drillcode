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
  /** Absent on a case you added with the expected value left blank: the reference solution supplies it. */
  expected?: unknown
  /** The expected value was filled in from the reference solution when the case was first run. */
  derived?: boolean
  custom?: boolean
}

export interface TestsSpec {
  kind: 'function' | 'operations'
  entry: string
  scaffolds: string[]
  /** Inputs the checker reads that are not arguments of the function: name to what it means. */
  extra_inputs?: Record<string, string>
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
  /** 'reference' when the expected value came from the reference solution. */
  expected_source?: 'reference' | null
  custom?: boolean
}

export type PyStatus = 'loading' | 'ready' | 'running' | 'restarting' | 'error'
