import { useEffect, useRef, useState } from 'react';
import { useDidUpdateEffect } from '../../hooks/useDidUpdateEffect';

interface MultiRangeProps {
  min: string;
  max: string;
  replaceFiltersObj(type: string, obj: Object): void;
}
const MultiRange = ({min, max, replaceFiltersObj}) => {
  const [val, setVal] = useState(null)
  const minRef = useRef();
  const maxRef = useRef();

  const updateValue = () => {
    // let _t = e.target;
    // _t.parentNode.style.setProperty(`--${_t.id}`, +_t.value);
    // setVal(_t.value)
    if(minRef.current && maxRef.current) {
      // replaceFiltersObj('year', {
      //   min: minRef.current.value,
      //   max: maxRef.current.value,
      // })
    }
    
  }
  const handleInput = (e) => {
    let _t = e.target;
    _t.parentNode.style.setProperty(`--${_t.id}`, +_t.value);
    setVal(_t.value)
  }
  useEffect(() => {
    // addEventListener('input', updateValue, false)
    // return () => {
    //   window.removeEventListener('input', updateValue);
    // }
  })

  useDidUpdateEffect(() => {
    // handle change event only after user
    // has stopped typing
    const timeOutId = setTimeout(() => {
      updateValue();
    }, 800);
    return () => clearTimeout(timeOutId);
  }, [val]);

  return (
    <div 
      className='multi-range-wrap'
      role='group'
      aria-labelledby='multi-lbl'
      style={{ 
        '--a': min,
        '--b': max,
        '--min': min,
        '--max': max
       }}>
    {/* <div id='multi-lbl'>Multi thumb slider:</div> */}
    <label className='sr-only' htmlFor='a'>Value A:</label>
    <input onInput={handleInput} ref={minRef} id='a' type='range' min={min} defaultValue={min} max={max} />
    <output htmlFor='a' style={{'--c': 'var(--a)'}}></output>
    <label className='sr-only' htmlFor='b'>Value B:</label>
    <input onInput={handleInput} ref={maxRef} id='b' type='range' min={min} defaultValue={max} max={max}/>
    <output htmlFor='b' style={{'--c': 'var(--b)'}}></output>
  </div>
  )
}
export default MultiRange;