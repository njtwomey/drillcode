import { ChevronDown } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import { Label } from '@/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

interface Props<T extends string> {
  label: string
  allLabel: string
  options: readonly T[]
  value: T[]
  onChange: (value: T[]) => void
  columns?: 1 | 2
  display?: (option: T) => string
}

/** A labelled dropdown of checkboxes. Empty selection means "all". */
export function MultiSelect<T extends string>({ label, allLabel, options, value, onChange, columns = 1, display }: Props<T>) {
  const show = display ?? ((o: T) => o)
  const toggle = (option: T) =>
    onChange(value.includes(option) ? value.filter((v) => v !== option) : [...value, option])
  return (
    <div className="space-y-1">
      <Label className="text-xs text-muted-foreground">{label}</Label>
      <Popover>
        <PopoverTrigger asChild>
          <Button variant="outline" size="sm" className="w-full min-w-40 justify-between font-normal">
            <span className="truncate">
              {value.length === 0 ? allLabel : value.length <= 2 ? value.map(show).join(', ') : `${value.length} selected`}
            </span>
            <span className="flex items-center gap-1">
              {value.length > 0 && <Badge variant="secondary">{value.length}</Badge>}
              <ChevronDown className="size-4 opacity-60" />
            </span>
          </Button>
        </PopoverTrigger>
        <PopoverContent align="start" className={columns === 2 ? 'w-80' : 'w-48'}>
          {/* Two columns fill top to bottom, then left to right, so the alphabetical order reads like a glossary. */}
          <div
            className="grid gap-x-2 gap-y-1.5"
            style={columns === 2 ? { gridAutoFlow: 'column', gridTemplateRows: `repeat(${Math.ceil(options.length / 2)}, auto)`, gridTemplateColumns: '1fr 1fr' } : undefined}
          >
            {options.map((option) => (
              <Label key={option} className="gap-2 text-sm font-normal">
                <Checkbox checked={value.includes(option)} onCheckedChange={() => toggle(option)} />
                {show(option)}
              </Label>
            ))}
          </div>
          {value.length > 0 && (
            <Button variant="ghost" size="sm" className="mt-2 w-full" onClick={() => onChange([])}>
              Clear selection
            </Button>
          )}
        </PopoverContent>
      </Popover>
    </div>
  )
}
