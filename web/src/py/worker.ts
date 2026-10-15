/// <reference lib="webworker" />
// One Pyodide instance per worker. Loaded from the CDN, not bundled.

const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/'

interface PyProxyFn {
  (...args: unknown[]): string
}
let runCaseJson: PyProxyFn | undefined

self.onmessage = async (event: MessageEvent) => {
  const msg = event.data
  if (msg.type === 'init') {
    try {
      const { loadPyodide } = await import(/* @vite-ignore */ PYODIDE_URL + 'pyodide.mjs')
      const pyodide = await loadPyodide({ indexURL: PYODIDE_URL })
      pyodide.FS.mkdirTree('/workbench')
      for (const [name, source] of Object.entries(msg.files as Record<string, string>)) {
        pyodide.FS.writeFile(`/workbench/${name}`, source)
      }
      pyodide.runPython('import sys\nsys.path.insert(0, "/workbench")')
      runCaseJson = pyodide.pyimport('runner').run_case_json
      self.postMessage({ type: 'ready' })
    } catch (error) {
      self.postMessage({ type: 'init-error', message: String(error) })
    }
  } else if (msg.type === 'run-case') {
    const { solutionSource, validatorSource, testsSpec, case: testCase, id } = msg
    try {
      const json = runCaseJson!(
        solutionSource,
        JSON.stringify(testsSpec),
        JSON.stringify(testCase),
        validatorSource ?? null,
      )
      self.postMessage({ type: 'result', id, result: JSON.parse(json) })
    } catch (error) {
      self.postMessage({
        type: 'result',
        id,
        result: {
          name: testCase.name, status: 'error', ms: 0, expected: testCase.expected, actual: null,
          message: String(error), stdout: '', stderr: '',
        },
      })
    }
  }
}
