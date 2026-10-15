/** mulberry32: a tiny seeded generator, so a shuffle can be repeated from its seed. */
export function seededRandom(seed: number): () => number {
  let a = seed >>> 0
  return () => {
    a = (a + 0x6d2b79f5) >>> 0
    let t = a
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

/** The seed for a new shuffle: the current time in milliseconds. */
export const timeSeed = (): number => Date.now()

/** Fisher-Yates on a copy; the same seed always gives the same order. */
export function seededShuffle<T>(items: readonly T[], seed: number): T[] {
  const random = seededRandom(seed)
  const out = [...items]
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1))
    ;[out[i], out[j]] = [out[j], out[i]]
  }
  return out
}
