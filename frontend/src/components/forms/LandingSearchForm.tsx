import { useState, useEffect, useRef } from "react";
import { StartTextAnimation } from "@utils/typewriter";
import getSite from "@utils/getSite";
import Close from "../buttons/Close";
import { SearchIcon } from "../svg/Icons";
import { SearchDropdown } from "./SearchDropdown";

import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";

interface SearchFormProps {
  placeholder?: string;
  handleSearchInput(term: string, filter?: string, filterValue?: string): void;
  input?: string;
}

const LandingSearchForm = ({ placeholder, input, handleSearchInput }: SearchFormProps) => {
  const [term, setTerm] = useState("");
  const [formFocus, setFormFocus] = useState(false);
  const inputRef = useRef(null);
  const formRef = useRef(null);
  // const site = getSite();
  const theme = useContext(ThemeContext);

  const clearSearch = () => {
    setTerm("");
  };

  const clearPlaceholder = () => {
    if (theme !== "cpr") return;
    inputRef.current.placeholder = "";
  };

  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };

  useEffect(() => {
    if (input) setTerm(input);
  }, [input]);

  useEffect(() => {
    if (inputRef.current) {
      const text = [placeholder ?? "Search full text of 3000+ laws and policies"];
      StartTextAnimation(0, text, inputRef.current);
    }
  }, [inputRef, placeholder]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (formRef.current && !formRef.current.contains(event.target)) {
        return setFormFocus(false);
      }
      setFormFocus(true);
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [formRef]);

  const wrapperCssClass = theme === "cpr" ? "text-white" : "text-indigo-400";

  const inputCssClass =
    theme === "cpr"
      ? "placeholder:text-white pr-16 text-2xl bg-transparent border-t-0 border-l-0 border-r-0 border-white border-b-2 focus:border-white focus:ring-0 w-full"
      : "py-3 pl-6 pr-16 w-full text-indigo-400 focus:ring-0";

  const buttonCssClass = theme === "cpr" ? "absolute top-0 right-0 -mt-1" : "absolute right-0 h-full pr-2 text-grey-700";

  return (
    <form data-cy="search-form" ref={formRef} onSubmit={(e) => e.preventDefault()}>
      <div className={`max-w-screen-lg mx-auto flex items-stretch relative ${wrapperCssClass}`}>
        <input data-cy="search-input" ref={inputRef} type="search" className={inputCssClass} value={term} onChange={onChange} onClick={clearPlaceholder} />
        {theme === "cpr" && term.length > 0 && (
          <div data-cy="search-clear-button" className="flex mx-2 shrink-0 absolute top-0 right-0 mr-20 z-20 h-full items-center">
            <Close onClick={clearSearch} size="16" />
          </div>
        )}
        <button className={buttonCssClass} onClick={() => handleSearchInput(term)}>
          <SearchIcon height="20" width="40" />
        </button>
        <SearchDropdown term={term} show={formFocus} handleSearchClick={handleSearchInput} largeSpacing />
      </div>
    </form>
  );
};
export default LandingSearchForm;
