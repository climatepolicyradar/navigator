import { FC, ReactNode } from "react";

type TProps = {
  children?: ReactNode; 
};

export const Divider: FC<TProps> = ({ children }) => {
  return (
    <div className="relative">
      <div className="bg-secondary-700 w-full h-px absolute top-1/2 z-0"></div>
      <div className="flex justify-center relative z-10">{children}</div>
    </div>
  );
};
