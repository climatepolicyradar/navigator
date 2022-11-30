import React, { FC, ReactNode } from "react";

type TProps = {
  children?: ReactNode;
};

const DropdownMenuWrapper: FC<TProps> = ({ children }) => {
  return (
    <div data-cy="dropdown-menu" className="rounded bg-indigo-100 shadow-xl shadow-black/10 py-2 w-48">
      {children}
    </div>
  );
};

export default DropdownMenuWrapper;
