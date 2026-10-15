import { ArrowRight } from 'lucide-react'
import { Link } from 'react-router'
import { cn } from '@/lib/utils'

const base =
  'inline-flex items-center gap-1 rounded-full border border-blue-600/30 px-2.5 py-0.5 text-xs font-medium text-blue-700 hover:bg-blue-600/10 dark:border-blue-400/30 dark:text-blue-300 dark:hover:bg-blue-400/10'

/** A pill that reads as a link and goes somewhere. */
export function ChipLink({ to, children, className }: { to: string; children: React.ReactNode; className?: string }) {
  return (
    <Link to={to} className={cn(base, className)}>
      {children}
      <ArrowRight className="size-3" />
    </Link>
  )
}

/** A pill that reads as a link and applies a filter. */
export function ChipButton({ onClick, title, children }: { onClick: () => void; title?: string; children: React.ReactNode }) {
  return (
    <button type="button" onClick={onClick} title={title} className={base}>
      {children}
    </button>
  )
}
