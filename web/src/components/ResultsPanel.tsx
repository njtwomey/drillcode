import { Badge } from '@/components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { StatusBadge } from '@/components/badges'
import type { CaseResult } from '@/lib/types'

const show = (v: unknown) => JSON.stringify(v)

export function ResultsTable({ results }: { results: CaseResult[] }) {
  return (
    <Table className="text-xs">
      <TableHeader>
        <TableRow>
          <TableHead>Case</TableHead>
          <TableHead className="w-20">Status</TableHead>
          <TableHead className="w-20 text-right">ms</TableHead>
          <TableHead>Details</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {results.map((r, i) => (
          <TableRow key={`${r.name}-${i}`}>
            <TableCell className="align-top">
              {r.name} {r.custom && <Badge variant="outline" className="ml-1">custom</Badge>}
            </TableCell>
            <TableCell className="align-top"><StatusBadge status={r.status} /></TableCell>
            <TableCell className="text-right align-top tabular-nums">{r.ms.toFixed(2)}</TableCell>
            <TableCell className="align-top">
              {r.status === 'fail' && (
                <div className="grid grid-cols-2 gap-2 font-mono">
                  <div><div className="text-muted-foreground">expected</div><div className="break-all">{show(r.expected)}</div></div>
                  <div><div className="text-muted-foreground">actual</div><div className="break-all">{show(r.actual)}</div></div>
                </div>
              )}
              {r.status === 'fail' && r.message && r.message !== 'Output does not match expected' && (
                <div className="mt-1 text-muted-foreground">{r.message}</div>
              )}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

export function Console({ results }: { results: CaseResult[] }) {
  const parts: string[] = []
  for (const r of results) {
    const body = [r.stdout, r.stderr, r.status === 'error' || r.status === 'timeout' ? r.message : '']
      .filter((s) => s && s.trim())
      .join('\n')
    if (body) parts.push(`# ${r.name}\n${body.trimEnd()}`)
  }
  return (
    <pre className="max-h-48 overflow-auto rounded-md border bg-muted/40 p-2 font-mono text-xs whitespace-pre-wrap">
      {parts.length ? parts.join('\n\n') : 'Console output (print, errors, tracebacks) appears here.'}
    </pre>
  )
}
