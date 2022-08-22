import { useState, useEffect, useRef } from "react";
import Close from "../buttons/Close";
import { SearchIcon } from "../svg/Icons";
import { StartTextAnimation } from "@utils/typewriter";
import { SearchDropdown } from "./SearchDropdown";

interface SearchFormProps {
  placeholder: string;
  handleSearchInput(term: string): void;
  input?: string;
}

const LandingSearchForm = ({ input, handleSearchInput }: SearchFormProps) => {
  const [term, setTerm] = useState("");
  const [formFocus, setFormFocus] = useState(false);
  const inputRef = useRef(null);
  const formRef = useRef(null);

  const typePlaceholder = () => {
    const text = ["Search full text of 3000+ laws and policies"];
    StartTextAnimation(0, text, inputRef.current);
  };

  const clearSearch = () => {
    setTerm("");
  };

  const clearPlaceholder = () => {
    inputRef.current.placeholder = "";
  };

  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };

  useEffect(() => {
    if (input) setTerm(input);
  }, [input]);

  useEffect(() => {
    if (inputRef.current) typePlaceholder();
  }, [inputRef]);

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

  return (
    <form data-cy="search-form" ref={formRef}>
      <div className="max-w-screen-lg mx-auto text-white flex items-stretch relative">
        <input
          data-cy="search-input"
          ref={inputRef}
          type="search"
          className="placeholder:text-white pr-16 text-2xl bg-transparent border-t-0 border-l-0 border-r-0 border-white border-b-2 focus:border-white focus:ring-0 w-full"
          value={term}
          onChange={onChange}
          onClick={clearPlaceholder}
        />
        {term.length > 0 && (
          <div data-cy="search-clear-button" className="flex text-indigo-300 mx-2 shrink-0 absolute top-0 right-0 mr-20 z-20 h-full items-center">
            <Close onClick={clearSearch} size="16" />
          </div>
        )}
        <button className="absolute top-0 right-0 -mt-1" onClick={() => handleSearchInput(term)}>
          <SearchIcon height="40" width="80" />
        </button>
        <SearchDropdown term={term} show={formFocus} handleSearchClick={() => handleSearchInput(term)} />
      </div>
    </form>
  );
};
export default LandingSearchForm;
