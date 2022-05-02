import { KebabMenuIcon } from '../Icons';
interface KebabProps {
  onClick(): void;
}
const Kebab = ({ onClick }) => {
  return (
    <button className="text-indigo-400" onClick={onClick}>
      <KebabMenuIcon />
    </button>
  );
};
export default Kebab;
