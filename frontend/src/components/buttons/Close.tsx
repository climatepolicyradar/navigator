import { CloseIcon } from '../Icons';

interface CloseProps {
  onClick(event: React.FormEvent<HTMLButtonElement>): void;
  size?: string;
}

const Close = ({ onClick, size = '20' }: CloseProps) => {
  return (
    <button
      className="focus:outline-none pointer-events-auto"
      onClick={onClick}
      style={{
        height: `${size}px`,
        width: `${size}px`,
      }}
    >
      {/* <img 
        src="/images/close.svg" 
        alt="Close icon"
        className="page-close"
     /> */}
      <CloseIcon />
    </button>
  );
};
export default Close;
