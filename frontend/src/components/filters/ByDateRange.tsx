import DateRangeOption from './DateRangeOption';

interface ByDateRangeProps {
  title: string;
}

const ByDateRange = ({ title }: ByDateRangeProps) => {
  return (
    <div>
      <div>{title}</div>
      {/* TODO: make labels translatable */}
      <div className="mt-4 grid lg:grid-cols-2 gap-2">
        <DateRangeOption
          id="last5"
          label="in last 5 years"
          name="date_range"
          value="last5"
        />
        <DateRangeOption
          id="last10"
          label="in last 10 years"
          name="date_range"
          value="last10"
        />
        <DateRangeOption
          id="specify"
          label="specify range"
          name="date_range"
          value="specify"
        />
      </div>
    </div>
  );
};
export default ByDateRange;
