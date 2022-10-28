// import getSite from "@utils/getSite";
import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";

type TProps = {
  detail: string;
  extraDetail?: string;
  amount: number;
  icon?: JSX.Element;
  onClick?: () => void;
};

export const KeyDetail = ({ detail, amount, icon, extraDetail, onClick }: TProps) => {
  const theme = useContext(ThemeContext);
  // const site = getSite();

  const handleOnClick = () => {
    if (onClick) onClick();
  };

  const cssClass = theme === "cpr" ? "text-blue-600" : "text-secondary-700";

  return (
    <div className={`key-detail bg-secondary-700 text-white flex p-3 shadow-md ${onClick ? "cursor-pointer" : ""}`} onClick={handleOnClick}>
      {icon && (
        <div className="flex items-center justify-center">
          <div className={`p-1 bg-white rounded-full w-[54px] h-[54px] flex items-center justify-center ${cssClass}`}>{icon}</div>
        </div>
      )}
      <div>
        <div className="flex items-center">
          <div className="text-lg ml-2">{detail}</div>
          <div className="ml-3 text-2xl font-bold drop-shadow">{amount}</div>
        </div>
        <div className="ml-2 text-sm">{extraDetail}</div>
      </div>
    </div>
  );
};
