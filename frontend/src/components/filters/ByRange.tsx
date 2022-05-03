import { useState } from 'react';
import { Range, getTrackBackground } from 'react-range';
interface ByRangeProps {
  title: string;
  type: string;
  min: number;
  max: number;
  handleChange(values: number[]): void;
}

const byRange = ({title, type, min = 1, max = 2, handleChange}: ByRangeProps) => {
  const [ values, setValues ] = useState([min, max]);

  return (
    <div>
      <div>{title}</div>
      <div className="mt-2">
        <Range 
          step={0.1}
          min={min}
          max={max}
          values={values}
          onChange={(values) => setValues(values)}
          onFinalChange={(values) => handleChange(values)}
          draggableTrack={true}
          renderTrack={({ props, children }) => (
            <div
              className="slider-track-outer"
              style={{
                ...props.style,
              }}
            >
              <div
                ref={props.ref}
                className="slider-track"
                style={{
                  background: getTrackBackground({
                    values,
                    colors: ['#e4e6ea', '#1f93ff', '#e4e6ea'],
                    min, max
  
                  }),
                  alignSelf: 'center'
                }}
              >
                {children}
              </div>
            </div>
          )}
          
          renderThumb={({index, props, isDragged}) => (
            <div {...props}
              className="slider-thumb-outer"
            >
              <div className="slider-thumb" />
              <output className="mt-6 block text-sm text-indigo-400">{values[index].toFixed(0)}</output>

            </div>
          )}
        />
      </div>
      
    </div>
    
  )
}

export default byRange;