import { convertDate } from '@utils/timedate';

interface Event {
  name: string;
  created_ts: string;
  date: string;
  description: string;
}
interface EventProps {
  event: Event;
  last: boolean;
  index: number;
}

function Event({ event, last, index }: EventProps) {
  const { name, created_ts } = event;
  const [year, _, month] = convertDate(created_ts);

  const even = (index + 1) % 2 === 0;

  const timelineStyles = last
    ? 'right-1/2 w-1/2'
    : index === 0
    ? 'left-1/2 w-1/2'
    : 'w-full';

  const renderText = (name: string, date: string) => (
    <div>
      <div className="w-[280px]">
        <h3 className="text-lg">{name}</h3>
        <p>{date}</p>
      </div>
    </div>
  );

  return (
    <div className="text-center w-[140px] relative flex-shrink-0">
      <div
        className={`h-[2px] bg-blue-500 absolute top-1/2 translate-y-[-1px] z-0 ${timelineStyles}`}
      />
      <div className="flex items-end justify-center h-[100px]">
        {!even && renderText(name, `${month} ${year}`)}
      </div>
      <div className="flex place-content-center h-full relative z-10">
        <div className="circle-container">
          <div
            className={index === 0 || last ? 'circle-large' : 'circle-small'}
          />
        </div>
      </div>
      <div className="flex items-start justify-center h-[100px]">
        {even && renderText(name, `${month} ${year}`)}
      </div>
    </div>
  );
}
export default Event;
