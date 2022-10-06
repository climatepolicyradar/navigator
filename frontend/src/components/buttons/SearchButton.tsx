import { FC } from "react";
import { SearchIcon } from "../svg/Icons";
import getSite from "@utils/getSite";

type TProps = {
  onClick?: () => void;
};

const SearchButton: FC<TProps> = ({ onClick, children }) => {
  const site = getSite();

  const handleOnClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    onClick();
  };

  const buttonCssClass = site === "cpr" ? "bg-blue-500 hover:bg-indigo-600" : "bg-secondary-700 hover:bg-primary-400";

  return (
    <button onClick={handleOnClick} type="submit" className={`text-white py-1 px-2 md:px-4 rounded-r-lg h-full transtion duration-300 shrink-0 ${buttonCssClass}`}>
      <SearchIcon height="20" width="40" />
      {children}
    </button>
  );
};

export default SearchButton;
