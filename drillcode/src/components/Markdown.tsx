import { Link } from 'react-router'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CodeBlock } from '@/components/CodeBlock'
import { techniqueBySlug } from '@/lib/techniques'

/** Markdown for tips pages. Inline `code` that names a technique becomes a link; fenced code is read-only CodeMirror. */
export function Markdown({ source, copyCode }: { source: string; copyCode?: boolean }) {
  return (
    <div className="space-y-3 text-sm leading-relaxed [&_ul]:list-disc [&_ul]:space-y-1 [&_ul]:pl-5 [&_ol]:list-decimal [&_ol]:space-y-1 [&_ol]:pl-5">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          pre: ({ children }) => <>{children}</>,
          code({ className, children }) {
            const text = String(children).replace(/\n$/, '')
            if (/language-python/.test(className ?? '')) return <CodeBlock code={text} copy={copyCode} />
            // Any other fence (```text diagrams) is shown as-is in a monospace box.
            if (/language-/.test(className ?? '') || text.includes('\n')) {
              return <pre className="my-3 overflow-x-auto rounded-md border bg-muted/40 p-3 font-mono text-[13px] leading-snug">{text}</pre>
            }
            if (techniqueBySlug.has(text)) {
              return (
                <Link to={`/tips/${text}`} className="font-medium text-blue-600 underline underline-offset-2 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300">
                  {techniqueBySlug.get(text)!.title}
                </Link>
              )
            }
            return <code className="rounded bg-muted px-1 py-0.5 font-mono text-[0.85em]">{children}</code>
          },
          h2: ({ children }) => <h2 className="mt-6 text-base font-semibold first:mt-0">{children}</h2>,
          h3: ({ children }) => <h3 className="mt-4 text-sm font-semibold">{children}</h3>,
          table: ({ children }) => <div className="overflow-x-auto"><table className="w-full border-collapse text-sm">{children}</table></div>,
          th: ({ children }) => <th className="border-b px-3 py-2 text-left font-medium">{children}</th>,
          td: ({ children }) => <td className="border-b px-3 py-2 align-top">{children}</td>,
        }}
      >
        {source}
      </ReactMarkdown>
    </div>
  )
}
