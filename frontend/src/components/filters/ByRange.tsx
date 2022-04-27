// import { YearRange } from "../../../model/yearRange";
import MultiRange from '../form-inputs/MultiRange';

interface ByRangeProps {
  title: string;
  type: string;
  min: string;
  max: string;
  // filters: YearRange;
  // replaceFiltersObj(type: string, obj: Object): void;
}
const ByRange = ({ title, type, min, max}: ByRangeProps) => {
  return (
    <div>
      <label className="text-sm">{title}</label>
      <div className="mt-4">
        <MultiRange 
          min={min}
          max={max}
        />
      </div>
      
    </div>
  )
}
export default ByRange;