import { FC } from "react";

export const SingleCol: FC = ({ children }) => {
  return <div className="mt-8 mx-auto max-w-screen-lg">{children}</div>;
};
