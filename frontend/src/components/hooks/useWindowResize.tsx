import { useEffect, useState } from 'react';

interface windowSizeInterface {
  width: number;
  height: number;
}

const useWindowResize = (): windowSizeInterface => {
  const [windowSize, setWindowSize] = useState({
    width: 0,
    height: 0,
  });
  useEffect(() => {
    // Handler to call on window resize
    function handleResize() {
      if (
        window.innerWidth !== windowSize.width ||
        window.innerHeight !== windowSize.height
      ) {
        // Set window width/height to state
        setWindowSize({
          width: window.innerWidth,
          height: window.innerHeight,
        });
      }
    }
    // Add event listener
    window.addEventListener('resize', handleResize);
    // Call handler right away so state gets updated with initial window size
    handleResize();
    // Remove event listener on cleanup
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  return windowSize;
};

export default useWindowResize;
