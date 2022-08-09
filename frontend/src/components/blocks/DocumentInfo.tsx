import Tooltip from '../tooltip';
import List from './List';

type TListType = {
  name: string;
  children?: TListChild[];
};

type TListChild = {
  parent: string;
  name: string;
};

type TDoucmentInfoProps = {
  heading: string;
  text?: string;
  list?: TListType[];
  id?: string;
  tooltip?: string;
  bulleted?: boolean;
};

function DocumentInfo({
  heading,
  text = '',
  list = [],
  id = '',
  tooltip = '',
  bulleted = false,
}: TDoucmentInfoProps) {
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
      {list.length ? (
        <List list={list} bulleted={bulleted} />
      ) : (
        <p className="text-indigo-500">{text}</p>
      )}
    </div>
  );
}

export default DocumentInfo;
