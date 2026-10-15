import { pythonSupportFiles } from '@/lib/catalogue'
import type { CaseResult, PyStatus, TestCase, TestsSpec } from '@/lib/types'

export const CASE_TIMEOUT_MS = 5000

interface Job {
  solutionSource: string
  validatorSource?: string
  spec: TestsSpec
}

/**
 * Owns the Pyodide web worker. Runs one case per message; if a case does not reply in
 * five seconds the worker is terminated, the case is a timeout, the rest are skipped,
 * and a fresh worker starts in the background.
 */
class PyRunner {
  status: PyStatus = 'loading'
  detail = ''
  private listeners = new Set<() => void>()
  private worker!: Worker
  private ready!: Promise<void>
  private nextId = 0

  constructor() {
    this.start()
  }

  subscribe = (listener: () => void) => {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }
  getSnapshot = () => this.status

  private setStatus(status: PyStatus, detail = '') {
    this.status = status
    this.detail = detail
    this.listeners.forEach((l) => l())
  }

  private start() {
    this.worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' })
    const worker = this.worker
    this.ready = new Promise<void>((resolve, reject) => {
      const onMessage = (event: MessageEvent) => {
        if (worker !== this.worker) return
        if (event.data.type === 'ready') {
          worker.removeEventListener('message', onMessage)
          this.setStatus('ready')
          resolve()
        } else if (event.data.type === 'init-error') {
          worker.removeEventListener('message', onMessage)
          this.setStatus('error', event.data.message)
          reject(new Error(event.data.message))
        }
      }
      worker.addEventListener('message', onMessage)
    })
    this.ready.catch(() => {})
    worker.postMessage({ type: 'init', files: pythonSupportFiles() })
  }

  private restart() {
    this.worker.terminate()
    this.setStatus('restarting')
    this.start()
  }

  private runOne(job: Job, testCase: TestCase): Promise<CaseResult | 'timeout'> {
    const id = this.nextId++
    const worker = this.worker
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        worker.removeEventListener('message', onMessage)
        resolve('timeout')
      }, CASE_TIMEOUT_MS)
      const onMessage = (event: MessageEvent) => {
        if (event.data.type !== 'result' || event.data.id !== id) return
        clearTimeout(timer)
        worker.removeEventListener('message', onMessage)
        resolve(event.data.result)
      }
      worker.addEventListener('message', onMessage)
      worker.postMessage({
        type: 'run-case',
        id,
        solutionSource: job.solutionSource,
        validatorSource: job.validatorSource,
        testsSpec: job.spec,
        case: testCase,
      })
    })
  }

  async runCases(job: Job, cases: TestCase[], onResult?: (results: CaseResult[]) => void): Promise<CaseResult[]> {
    await this.ready
    this.setStatus('running')
    const results: CaseResult[] = []
    const base = (c: TestCase) => ({
      name: c.name, ms: 0, expected: c.expected, actual: null, message: '', stdout: '', stderr: '', custom: c.custom,
    })
    for (let i = 0; i < cases.length; i++) {
      const outcome = await this.runOne(job, cases[i])
      if (outcome === 'timeout') {
        results.push({ ...base(cases[i]), status: 'timeout', ms: CASE_TIMEOUT_MS, message: 'Time limit exceeded (5 s). The worker was restarted.' })
        for (const rest of cases.slice(i + 1)) results.push({ ...base(rest), status: 'skipped' })
        onResult?.([...results])
        this.restart()
        return results
      }
      results.push({ ...outcome, custom: cases[i].custom })
      onResult?.([...results])
    }
    this.setStatus('ready')
    return results
  }
}

export const pyRunner = new PyRunner()
