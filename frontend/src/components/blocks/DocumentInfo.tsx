import Tooltip from "../tooltip";
import List from "./List";

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

const DocumentInfo = ({ heading, text = "", list = [], id = "", tooltip = "" }: DoucmentInfoProps) => {
  const renderList = (list: ListType[]) => {
    return list.map((item, i) => [i > 0 && ", ", item.name]);
  };

  return (
    <div className="mt-4">
      <h4 className="text-base text-indigo-400 font-semibold flex">
        {heading}
        {tooltip.length > 0 && (
          <div className="ml-1 font-normal">
            <Tooltip id={id} tooltip={tooltip} />
          </div>
        )}
      </h4>
      {/* {list.length ? <List list={list} /> : <p className="text-indigo-500">{text}</p>} */}
      <p className="text-indigo-500">{list.length ? renderList(list) : text}</p>
    </div>
  );
};

export default DocumentInfo;
