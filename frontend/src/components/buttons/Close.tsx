import React from "react";
import { CloseIcon } from "../svg/Icons";

interface CloseProps {
  onClick(): void;
  size?: string;
}

const Close = ({ onClick, size = "20" }: CloseProps) => {
  
  const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    onClick();
  };
  return (
    <button
      className="focus:outline-none pointer-events-auto"
      onClick={handleClick}
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
