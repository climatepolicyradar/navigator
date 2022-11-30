import { FC, ReactNode } from "react";
import { HERO_DEFAULT_HEIGHT } from "@constants/hero";

type TProps = {
  height?: number;
  children?: ReactNode;
}

export const Hero: FC<TProps> = ({ children, height = HERO_DEFAULT_HEIGHT }) => {
  return <section className={`absolute inset-0 z-10 flex flex-col items-center justify-center`} style={{minHeight: height}}>{children}</section>;
};