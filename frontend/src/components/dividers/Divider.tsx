import { FC } from "react";

export const Divider: FC = ({ children }) => {
  return (
    <div className="relative">
      <div className="bg-blue-600 w-full h-px absolute top-1/2 z-0"></div>
      <div className="flex justify-center relative z-10">{children}</div>
    </div>
  );
};
