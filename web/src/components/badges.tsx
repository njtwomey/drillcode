import { Badge } from '@/components/ui/badge'
import type { CaseStatus, Difficulty } from '@/lib/types'
import { cn } from '@/lib/utils'

const difficultyClass: Record<Difficulty, string> = {
  easy: 'border-green-600/40 text-green-700 dark:text-green-400',
  medium: 'border-amber-600/40 text-amber-700 dark:text-amber-400',
  hard: 'border-red-600/40 text-red-700 dark:text-red-400',
}
export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  return <Badge variant="outline" className={cn('capitalize', difficultyClass[difficulty])}>{difficulty}</Badge>
}

const statusClass: Record<CaseStatus, string> = {
  pass: 'bg-green-600 text-white hover:bg-green-600',
  fail: 'bg-red-600 text-white hover:bg-red-600',
  error: 'bg-red-800 text-white hover:bg-red-800',
  timeout: 'bg-amber-600 text-white hover:bg-amber-600',
  skipped: 'bg-muted text-muted-foreground hover:bg-muted',
}
export function StatusBadge({ status }: { status: CaseStatus }) {
  return <Badge className={statusClass[status]}>{status}</Badge>
}
