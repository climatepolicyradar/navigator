import { FC, ReactNode } from "react";

type TProps = {
  children?: ReactNode;
};

export const Timeline: FC<TProps> = ({ children }) => {
  return (
    <div className="mt-4">
      <div className="flex place-content-center bg-offwhite rounded border border-lineBorder drop-shadow-lg p-4">
        <div className="flex items-center overflow-x-auto px-[70px]">{children}</div>
      </div>
    </div>
  );
};
