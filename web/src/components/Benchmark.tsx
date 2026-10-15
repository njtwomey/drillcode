import { Gauge } from 'lucide-react'
import { useState } from 'react'
import { Chart } from '@/components/Chart'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import type { CaseResult, TestCase } from '@/lib/types'

interface Props {
  disabled: boolean
  runSuite: () => Promise<{ results: CaseResult[]; cases: TestCase[] } | null>
}

interface Summary {
  names: string[]
  meanMs: number[]
  passFraction: number[]
  totals: number[]
}

export function Benchmark({ disabled, runSuite }: Props) {
  const [runs, setRuns] = useState(10)
  const [busy, setBusy] = useState(false)
  const [progress, setProgress] = useState(0)
  const [summary, setSummary] = useState<Summary | null>(null)

  async function start() {
    setBusy(true)
    setSummary(null)
    const all: CaseResult[][] = []
    const totals: number[] = []
    for (let i = 0; i < runs; i++) {
      setProgress(i)
      const t0 = performance.now()
      const outcome = await runSuite()
      if (!outcome) break
      totals.push(performance.now() - t0)
      all.push(outcome.results)
      if (outcome.results.some((r) => r.status === 'timeout')) break
    }
    if (all.length) {
      const names = all[0].map((r) => r.name)
      setSummary({
        names,
        meanMs: names.map((_, c) => all.reduce((sum, run) => sum + (run[c]?.ms ?? 0), 0) / all.length),
        passFraction: names.map((_, c) => all.filter((run) => run[c]?.status === 'pass').length / all.length),
        totals,
      })
    }
    setBusy(false)
  }

  const x = (names: string[]) => ({ type: 'category' as const, data: names, axisLabel: { rotate: 35, interval: 0 } })
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 text-sm">
        <Input
          type="number" min={1} max={500} className="h-8 w-20" value={runs}
          onChange={(e) => setRuns(Math.max(1, Math.min(500, Number(e.target.value) || 1)))}
        />
        <Button size="sm" variant="outline" disabled={disabled || busy} onClick={start}>
          <Gauge /> {busy ? `Run ${progress + 1} of ${runs}` : 'Benchmark'}
        </Button>
      </div>
      {summary && (
        <div className="grid gap-2 lg:grid-cols-3">
          <Chart height={240} option={{ title: { text: 'Mean ms per case', textStyle: { fontSize: 12 } }, tooltip: {}, xAxis: x(summary.names), yAxis: { type: 'value' }, series: [{ type: 'bar', data: summary.meanMs.map((v) => +v.toFixed(3)) }] }} />
          <Chart height={240} option={{ title: { text: 'Pass fraction per case', textStyle: { fontSize: 12 } }, tooltip: {}, xAxis: x(summary.names), yAxis: { type: 'value', min: 0, max: 1 }, series: [{ type: 'bar', data: summary.passFraction }] }} />
          <Chart height={240} option={{ title: { text: 'Total wall time per run (ms)', textStyle: { fontSize: 12 } }, tooltip: { trigger: 'axis' }, xAxis: { type: 'category', data: summary.totals.map((_, i) => i + 1) }, yAxis: { type: 'value' }, series: [{ type: 'line', data: summary.totals.map((v) => +v.toFixed(1)) }] }} />
        </div>
      )}
    </div>
  )
}
