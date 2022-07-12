import { convertDate } from "@utils/timedate";

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

const Event = ({ event, last, index }: EventProps) => {
  const { name, created_ts } = event;
  const [year, _, month] = convertDate(created_ts);

  const even = (index + 1) % 2 === 0;

  const timelineStyles = last ? "right-1/2 w-1/2" : index === 0 ? "left-1/2 w-1/2" : "w-full";

  return (
    <div className="text-center w-[200px] shrink-0 relative h-[140px]">
      <div className={`h-[2px] bg-blue-500 absolute top-1/2 translate-y-[-1px] z-0 ${timelineStyles}`} />
      <div className={`absolute ${even ? "inset-x-0 top-0" : "inset-x-0 bottom-0"} w-[200%] left-[-50%]`}>
        <h3 className="text-xl">{name}</h3>
        <p>{month + " " + year}</p>
      </div>
      <div className="flex place-content-center h-full relative z-10">
        <div className="circle-container">
          <div className={index === 0 || last ? "circle-large" : "circle-small"}></div>
        </div>
      </div>
    </div>
  );
};
export default Event;
