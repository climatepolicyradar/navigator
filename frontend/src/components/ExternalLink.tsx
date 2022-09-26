import { FC } from "react";

type TProps = {
  url: string;
  className?: string;
};

export const ExternalLink: FC<TProps> = ({ url, className, children }) => {
  return (
    <a href={url} target="_blank" rel="noopener noreferrer nofollow" className={className}>
      {children}
    </a>
  );
};
