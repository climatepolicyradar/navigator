import { KebabMenuIcon } from '../Icons';
interface KebabProps {
  onClick(): void;
}
const Kebab = ({ onClick }) => {
  return (
    <button
      className="bg-indigo-500 text-white p-3 shadow rounded-full"
      onClick={onClick}
    >
      <KebabMenuIcon />
    </button>
  );
};
export default Kebab;
