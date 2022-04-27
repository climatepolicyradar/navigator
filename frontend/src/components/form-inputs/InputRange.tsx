import { useState } from 'react';
import { Range, getTrackBackground } from 'react-range';

const InputRange = ({title}) => {
  const [ values, setValues ] = useState([1981, 2010]);
  const MIN = 1947;
  const MAX = 2022;
  const onMouseDown = (e) => {
    console.log(e.target)
  }
  return (
    <div>
      <div>{title}</div>
      <div className="mt-2">
        <Range 
          step={0.1}
          min={MIN}
          max={MAX}
          values={values}
          onChange={(values) => setValues(values)}
          draggableTrack={true}
          renderTrack={({props, children}) => (
            <div
            {...props}
              className="slider-track-outer"
            >
              <div ref={props.ref} className="slider-track" style={{background: getTrackBackground({ values, colors: ['#e4e6ea', '#1f93ff', '#e4e6ea'],
                  min: MIN,
                  max: MAX, }), alignSelf: 'center'}}>
                {children}
              </div>
              
            </div>
          )}
          renderThumb={({index, props, isDragged}) => (
            <div {...props}
              className="slider-thumb"
            >
              <div className="mt-10">
                {values[index]}
              </div>
              
            </div>
          )}
        />
      </div>
      
    </div>
    
  )
}

export default InputRange;