import { FC, ReactNode } from "react";

type TProps = {
  url: string;
  className?: string;
  children?: ReactNode;
};

export const ExternalLink: FC<TProps> = ({ url, className, children }) => {
  return (
    <a href={url} target="_blank" rel="noopener noreferrer nofollow" className={className}>
      {children}
    </a>
  );
};
