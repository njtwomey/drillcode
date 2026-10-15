import { useEffect, useRef } from 'react'
import { closeBrackets, closeBracketsKeymap } from '@codemirror/autocomplete'
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands'
import { python } from '@codemirror/lang-python'
import {
  bracketMatching, defaultHighlightStyle, indentOnInput, indentUnit, syntaxHighlighting,
} from '@codemirror/language'
import { Annotation, Compartment, EditorState, Prec } from '@codemirror/state'
import { oneDark } from '@codemirror/theme-one-dark'
import {
  EditorView, highlightActiveLine, highlightActiveLineGutter, keymap, lineNumbers,
} from '@codemirror/view'

interface Props {
  value: string
  onChange: (value: string) => void
  onRun: () => void
  dark: boolean
}

// Marks edits made by the app (mode switch, Reset) so they are not saved as user drafts.
const external = Annotation.define<boolean>()

const baseTheme = EditorView.theme({
  '&': { height: '100%', fontSize: '14px' },
  '.cm-scroller': { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' },
  '&.cm-focused': { outline: 'none' },
})
const lightTheme = [
  syntaxHighlighting(defaultHighlightStyle),
  EditorView.theme({ '.cm-gutters': { backgroundColor: 'transparent', border: 'none' } }),
]
const darkTheme = [oneDark, EditorView.theme({ '&': { backgroundColor: 'transparent' } }, { dark: true })]

/** CodeMirror 6, Python only; closeBrackets is the only automation (no completion). */
export function CodeEditor({ value, onChange, onRun, dark }: Props) {
  const host = useRef<HTMLDivElement>(null)
  const view = useRef<EditorView | null>(null)
  const themeCompartment = useRef(new Compartment())
  const callbacks = useRef({ onChange, onRun })
  callbacks.current = { onChange, onRun }

  useEffect(() => {
    const editor = new EditorView({
      parent: host.current!,
      state: EditorState.create({
        doc: value,
        extensions: [
          lineNumbers(),
          EditorView.lineWrapping,
          highlightActiveLine(),
          highlightActiveLineGutter(),
          history(),
          indentOnInput(),
          indentUnit.of('    '),
          EditorState.tabSize.of(4),
          closeBrackets(),
          bracketMatching(),
          python(),
          baseTheme,
          themeCompartment.current.of(dark ? darkTheme : lightTheme),
          Prec.highest(
            keymap.of([{ key: 'Mod-Enter', run: () => (callbacks.current.onRun(), true) }]),
          ),
          keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
          EditorView.updateListener.of((update) => {
            if (update.docChanged && !update.transactions.some((t) => t.annotation(external))) callbacks.current.onChange(update.state.doc.toString())
          }),
        ],
      }),
    })
    view.current = editor
    return () => editor.destroy()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  useEffect(() => {
    const editor = view.current
    if (editor && editor.state.doc.toString() !== value) {
      editor.dispatch({ changes: { from: 0, to: editor.state.doc.length, insert: value }, annotations: external.of(true) })
    }
  }, [value])

  useEffect(() => {
    view.current?.dispatch({ effects: themeCompartment.current.reconfigure(dark ? darkTheme : lightTheme) })
  }, [dark])

  return <div ref={host} className="h-full min-h-0 overflow-hidden rounded-md border bg-background" />
}
