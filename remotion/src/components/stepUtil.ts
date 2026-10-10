// Step-based visuals (ArrayViz, TreeViz, GraphViz, StackQueueViz) ke liye common helper.
// stepAt: har step kab shuru hota hai (seconds, to_remotion.py narration ke word timing se nikalta hai).
export function activeStepIndex(n: number, stepAt: number[] | undefined, sec: number): number {
  if (n === 0) return -1;
  if (!stepAt || stepAt.length !== n) return 0;
  let a = 0;
  for (let i = 0; i < n; i++) if (sec >= stepAt[i]) a = i;
  return a;
}
