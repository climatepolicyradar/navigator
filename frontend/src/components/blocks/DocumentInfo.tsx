import List from './List';
interface ListType {
  name: string;
  children?: string[];
}
interface DoucmentInfoProps {
  heading: string;
  text?: string;
  list?: ListType[];
}

const DocumentInfo = ({ heading, text = '', list = [] }) => {
  return (
    <div className="mt-6">
      <h4 className="text-base text-indigo-600 font-medium">{heading}</h4>
      {list.length ? (
        <List list={list} />
      ) : (
        <p className="text-indigo-500">{text}</p>
      )}
    </div>
  );
};
export default DocumentInfo;
