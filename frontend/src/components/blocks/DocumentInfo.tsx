import Tooltip from '../tooltip';
import List from './List';
interface ListType {
  name: string;

  children?: string[];
}
interface DoucmentInfoProps {
  heading: string;
  text?: string;
  list?: ListType[];
  id?: string;
  tooltip?: string;
}

const DocumentInfo = ({
  heading,
  text = '',
  list = [],
  id = '',
  tooltip = '',
}: DoucmentInfoProps) => {
  return (
    <div className="mt-6">
      <h4 className="text-base text-indigo-600 font-medium flex">
        {heading}
        {tooltip.length > 0 && (
          <div className="ml-1 font-normal">
            <Tooltip id={id} tooltip={tooltip} />
          </div>
        )}
      </h4>
      {list.length ? (
        <List list={list} />
      ) : (
        <p className="text-indigo-500">{text}</p>
      )}
    </div>
  );
};
export default DocumentInfo;
