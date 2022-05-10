import Link from 'next/link';
import { DownLongArrowIcon } from '../Icons';

interface Event {
  date: string;
  status: string;
  description: string;
  document_url?: string;
}
interface EventProps {
  event: Event;
  last: boolean;
}
const Event = ({ event, last }) => {
  const { date, status, description, document_url = null } = event;
  const arr = date.split('/');
  const year = arr[0];
  const month_day = `${arr[1]}/${arr[2]}`;
  return (
    <div className="flex mt-1">
      <div className="flex flex-col items-center w-1/2">
        <div className="w-full bg-blue-200 rounded-2xl px-8 py-1 flex flex-col items-center text-indigo-600 mb-2">
          <div className="text-2xl font-medium">{year}</div>
          <div>{month_day}</div>
        </div>
        {!last && <DownLongArrowIcon />}
      </div>
      <div className="ml-8">
        <div className="text-indigo-600">{status}</div>
        <div className="text-sm">{description}</div>
      </div>
    </div>
  );
};
export default Event;
