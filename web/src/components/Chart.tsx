import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, LegendComponent, TitleComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import ReactEChartsCoreModule from 'echarts-for-react/lib/core'
import type { EChartsOption } from 'echarts'
import { Component, type ReactNode } from 'react'
import { useStore } from '@/lib/store'

echarts.use([BarChart, LineChart, GridComponent, TitleComponent, TooltipComponent, LegendComponent, CanvasRenderer])

// echarts-for-react is CommonJS: depending on interop the component sits under `.default`.
const ReactEChartsCore = (
  'default' in ReactEChartsCoreModule ? (ReactEChartsCoreModule as { default: unknown }).default : ReactEChartsCoreModule
) as typeof ReactEChartsCoreModule

/** A broken chart should not blank the whole page. */
class ChartBoundary extends Component<{ children: ReactNode }, { error?: Error }> {
  state: { error?: Error } = {}
  static getDerivedStateFromError(error: Error) {
    return { error }
  }
  render() {
    if (this.state.error) return <p className="text-xs text-destructive">Chart failed: {this.state.error.message}</p>
    return this.props.children
  }
}

export function Chart(props: { option: EChartsOption; height?: number }) {
  return (
    <ChartBoundary>
      <ChartInner {...props} />
    </ChartBoundary>
  )
}

/** Static chart: no animation, colours follow the light/dark theme. */
function ChartInner({ option, height = 220 }: { option: EChartsOption; height?: number }) {
  const dark = useStore((s) => s.theme === 'dark')
  const text = dark ? '#a3a3a3' : '#525252'
  const line = dark ? '#404040' : '#e5e5e5'
  const themed: EChartsOption = {
    animation: false,
    backgroundColor: 'transparent',
    textStyle: { color: text },
    color: dark ? ['#e5e5e5', '#525252', '#f87171'] : ['#262626', '#d4d4d4', '#dc2626'],
    grid: { left: 44, right: 12, top: 28, bottom: 52 },
    ...option,
  }
  return (
    <ReactEChartsCore
      echarts={echarts}
      option={themed}
      notMerge
      style={{ height, width: '100%' }}
      opts={{ renderer: 'canvas' }}
      key={dark ? 'dark' : 'light'}
      theme={undefined}
      lazyUpdate
      onChartReady={(chart) => chart.setOption({ xAxis: { axisLine: { lineStyle: { color: line } } } })}
    />
  )
}
