import { useState, useEffect, useRef, useContext } from "react";
import Close from "../buttons/Close";
import { SearchIcon } from "../svg/Icons";
import { SearchDropdown } from "./SearchDropdown";
import { ThemeContext } from "@context/ThemeContext";

interface SearchFormProps {
  placeholder?: string;
  handleSearchInput(term: string, filter?: string, filterValue?: string): void;
  input?: string;
}

const LandingSearchForm = ({ placeholder, input, handleSearchInput }: SearchFormProps) => {
  const [term, setTerm] = useState("");
  const [formFocus, setFormFocus] = useState(false);
  const [showAnimation, setShowAnimation] = useState(true);
  const formRef = useRef(null);
  const theme = useContext(ThemeContext);

  const clearSearch = () => {
    setTerm("");
  };

  const clearPlaceholderAnimation = () => {
    if (theme !== "cpr") return;
    setShowAnimation(false);
  };

  const showPlaceholderAnimation = () => {
    if (theme !== "cpr") return;
    if (term.length === 0) setShowAnimation(true);
  };

  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };

  useEffect(() => {
    if (input) setTerm(input);
  }, [input]);

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

  const buttonCssClass = theme === "cpr" ? "absolute top-0 right-0 h-full" : "absolute right-0 h-full pr-2 text-grey-700";
  const displayPlaceholder = placeholder ?? "Search full text of 3000+ laws and policies";

  return (
    <form data-cy="search-form" ref={formRef} onSubmit={(e) => e.preventDefault()}>
      <div className={`max-w-screen-lg mx-auto flex items-stretch relative ${wrapperCssClass}`}>
        <input
          id="landingPage-searchInput"
          data-analytics="landingPage-searchInput"   
          data-cy="search-input"   
          type="search"
          className={inputCssClass}
          value={term}
          onChange={onChange}
          onFocus={clearPlaceholderAnimation}
          onBlur={showPlaceholderAnimation}
          placeholder={displayPlaceholder}
        />
        {theme === "cpr" && showAnimation && term.length === 0 && <div className="search-animated-placeholder">{displayPlaceholder}</div>}
        {theme === "cpr" && term.length > 0 && (
          <div data-cy="search-clear-button" className="flex mx-2 shrink-0 absolute top-0 right-0 mr-14 z-20 h-full items-center">
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
