import { FC } from "react";
import { SearchIcon } from "../svg/Icons";

type TProps = {
  onClick?: () => void;
};

const SearchButton: FC<TProps> = ({ onClick, children }) => {
  
  const handleOnClick = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    onClick();
  };

  return (
    <button onClick={handleOnClick} type="submit" className="bg-blue-500 text-white py-1 px-2 md:px-4 rounded-r-lg h-full hover:bg-indigo-600 transtion duration-300 shrink-0">
      <SearchIcon height="20" width="40" />
      {children}
    </button>
  );
};

export default SearchButton;
