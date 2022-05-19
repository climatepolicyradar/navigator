import { CloseIcon } from '../svg/Icons';

interface CloseProps {
  onClick(event: React.FormEvent<HTMLButtonElement>): void;
  size?: string;
}

const Close = ({ onClick, size = '20' }: CloseProps) => {
  return (
    <button
      className="focus:outline-none pointer-events-auto"
      onClick={onClick}
      type="button"
      style={{
        height: `${size}px`,
        width: `${size}px`,
      }}
    >
      <CloseIcon height={size} width={size} />
    </button>
  );
};
export default Close;
