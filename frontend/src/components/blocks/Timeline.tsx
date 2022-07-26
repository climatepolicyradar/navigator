import { FC } from "react";

export const Timeline: FC = ({ children }) => {
  return (
    <div className="mt-8">
      <div className="flex place-content-center bg-offwhite rounded border border-blue-200 drop-shadow-lg p-4">
        <div className="flex items-center overflow-x-auto px-[70px]">{children}</div>
      </div>
    </div>
  );
};
