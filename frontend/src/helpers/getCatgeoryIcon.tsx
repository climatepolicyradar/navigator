import { TCategory } from "@types";
import { LawIcon, PolicyIcon, CaseIcon, TargetIcon } from "@components/svg/Icons";

export const getCategoryIcon = (category: TCategory, size?: string) => {
  let icon: JSX.Element;
  switch (category) {
    case "Cases":
      icon = <CaseIcon height={size} width={size} />;
      break;
    case "Laws":
      icon = <LawIcon height={size} width={size} />;
      break;
    case "Policies":
      icon = <PolicyIcon height={size} width={size} />;
      break;
    case "Targets":
      icon = <TargetIcon height={size} width={size} />;
      break;
  }
  return icon;
};
