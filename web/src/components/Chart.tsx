import { BarChart, LineChart } from 'echarts/charts'
import { GridComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import ReactEChartsCore from 'echarts-for-react/lib/core'
import type { EChartsOption } from 'echarts'
import { useStore } from '@/lib/store'

echarts.use([BarChart, LineChart, GridComponent, TooltipComponent, LegendComponent, CanvasRenderer])

/** Static chart: no animation, colours follow the light/dark theme. */
export function Chart({ option, height = 220 }: { option: EChartsOption; height?: number }) {
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
