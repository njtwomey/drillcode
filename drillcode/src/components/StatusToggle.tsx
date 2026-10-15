import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group'
import type { StatusFilter } from '@/lib/store'

/** All / not done yet / already done. */
export function StatusToggle({ value, onChange }: { value: StatusFilter; onChange: (value: StatusFilter) => void }) {
  return (
    <ToggleGroup type="single" variant="outline" size="sm" value={value} onValueChange={(v) => v && onChange(v as StatusFilter)}>
      <ToggleGroupItem value="all">All</ToggleGroupItem>
      <ToggleGroupItem value="todo">Not done yet</ToggleGroupItem>
      <ToggleGroupItem value="done">Done</ToggleGroupItem>
    </ToggleGroup>
  )
}
