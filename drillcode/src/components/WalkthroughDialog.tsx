import { BookOpen, ExternalLink } from 'lucide-react'
import { Link } from 'react-router'
import { Markdown } from '@/components/Markdown'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { useState } from 'react'
import { hasWalkthrough } from '@/lib/catalogue'
import { useWalkthrough } from '@/lib/useWalkthrough'

/** The walkthrough as a modal: a long, diagram-heavy explanation that should not push the code off screen. */
export function WalkthroughDialog({ slug, title }: { slug: string; title: string }) {
  const [open, setOpen] = useState(false)
  const { text, loading } = useWalkthrough(slug, open)
  if (!hasWalkthrough(slug)) return null
  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button size="sm" variant="outline"><BookOpen /> Walkthrough</Button>
      </DialogTrigger>
      <DialogContent className="max-h-[88vh] w-[min(56rem,calc(100vw-2rem))] max-w-none overflow-y-auto sm:max-w-none">
        <DialogHeader>
          <DialogTitle>{title}: walkthrough</DialogTitle>
          <DialogDescription>
            Why the solution is shaped this way, with a traced example.{' '}
            <Link to={`/p/${slug}/read`} className="inline-flex items-center gap-1 underline">
              Open as a page <ExternalLink className="size-3" />
            </Link>
          </DialogDescription>
        </DialogHeader>
        {loading ? <p className="text-sm text-muted-foreground">Loading…</p> : text && <Markdown source={text} />}
      </DialogContent>
    </Dialog>
  )
}
