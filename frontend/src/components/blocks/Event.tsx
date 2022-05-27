import { DownLongArrowIcon } from '../svg/Icons';
import { convertDate } from '../../utils/timedate';

interface Event {
  name: string;
  created_ts: string;
  date: string;
  description: string;
}
interface EventProps {
  event: Event;
  last: boolean;
}
const Event = ({ event, last }: EventProps) => {
  const { name, created_ts, description } = event;
  const [year, day, month] = convertDate(created_ts);

  return (
    <div className="flex mt-1">
      <div className="flex flex-col items-center w-1/2">
        <div className="w-full bg-blue-200 rounded-2xl px-8 py-1 flex flex-col items-center text-indigo-600 mb-2">
          <div className="text-2xl font-medium">{year}</div>
          <div>{`${day} ${month}`}</div>
        </div>
        {!last && <DownLongArrowIcon />}
      </div>
      <div className="ml-4 shrink-0 w-1/2">
        <div className="text-indigo-500">{name}</div>
      </div>
    </div>
  );
};
export default Event;
