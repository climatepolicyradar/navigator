import { string } from 'yup/lib/locale';

interface PillProps {
  text: string;
}

const Pill = ({ text }: PillProps) => {
  return (
    <span className="bg-blue-500 uppercase text-sm font-bold py-2 px-4 text-white rounded-2xl tracking-widest">
      {text}
    </span>
  );
};
export default Pill;
