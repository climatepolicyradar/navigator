import { useEffect, useRef } from 'react';

// this custom hook only checks if inputs change, and does not get trigged on initial render
export function useDidUpdateEffect(fn, inputs) {
  const didMountRef = useRef(false);

  useEffect(() => {
    if (didMountRef.current) return fn();
    else didMountRef.current = true;
  }, inputs);
}
