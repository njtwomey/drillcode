import { python } from '@codemirror/lang-python'
import { defaultHighlightStyle, syntaxHighlighting } from '@codemirror/language'
import { Compartment, EditorState } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark'
import { EditorView } from '@codemirror/view'
import { Check, Copy } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Button } from '@/components/ui/button'
import { useStore } from '@/lib/store'

const theme = EditorView.theme({
  '&': { fontSize: '13px' },
  '.cm-scroller': { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', overflow: 'auto' },
  '.cm-content': { padding: '8px 0' },
})
const light = [syntaxHighlighting(defaultHighlightStyle), EditorView.theme({ '&': { backgroundColor: 'transparent' } })]
const dark = [oneDark, EditorView.theme({ '&': { backgroundColor: 'transparent' } }, { dark: true })]

/** Read-only CodeMirror, so highlighting matches the editor. */
export function CodeBlock({ code, copy }: { code: string; copy?: boolean }) {
  const host = useRef<HTMLDivElement>(null)
  const view = useRef<EditorView | null>(null)
  const themeSlot = useRef(new Compartment())
  const isDark = useStore((s) => s.theme === 'dark')
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    const editor = new EditorView({
      parent: host.current!,
      state: EditorState.create({
        doc: code,
        extensions: [python(), theme, themeSlot.current.of(isDark ? dark : light), EditorState.readOnly.of(true), EditorView.editable.of(false)],
      }),
    })
    view.current = editor
    return () => editor.destroy()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [code])

  useEffect(() => {
    view.current?.dispatch({ effects: themeSlot.current.reconfigure(isDark ? dark : light) })
  }, [isDark])

  async function copyCode() {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      /* clipboard unavailable: nothing to do */
    }
  }

  return (
    <div className="relative my-3 overflow-hidden rounded-md border">
      <div ref={host} />
      {copy && (
        <Button size="sm" variant="outline" className="absolute top-2 right-2 h-7 bg-background/80" onClick={copyCode}>
          {copied ? <Check /> : <Copy />} {copied ? 'Copied' : 'Copy'}
        </Button>
      )}
    </div>
  )
}
