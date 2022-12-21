import React, { useState, useEffect, useRef } from "react";
import Close from "../buttons/Close";
import SearchButton from "../buttons/SearchButton";
import useWindowResize from "@hooks/useWindowResize";
import { SearchDropdown } from "./SearchDropdown";

interface SearchFormProps {
  placeholder: string;
  handleSearchInput(term: string): void;
  handleSuggestion(term: string, filter?: string, filterValue?: string): void;
  input?: string;
}

const SearchForm = ({ input, placeholder, handleSearchInput, handleSuggestion }: SearchFormProps) => {
  const [term, setTerm] = useState("");
  const [formFocus, setFormFocus] = useState(false);
  const formRef = useRef(null);
  const windowSize = useWindowResize();

  const clearSearch = () => {
    setTerm("");
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTerm(e.currentTarget.value);
  };

  const handleSuggestionClick = (term: string, filter?: string, filterValue?: string) => {
    setTerm(term);
    handleSuggestion(term, filter, filterValue);
  }

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

  return (
    <form data-cy="search-form" ref={formRef} onSubmit={(e) => e.preventDefault()}>
      <div className="relative shadow-md rounded-lg bg-white flex items-stretch z-40">
        <input
          data-analytics="seachPage-searchInput"
          data-cy="search-input"
          className="analytics-searchPage-searchInput bg-transparent text-indigo-600 appearance-none py-2 pl-2 z-10 rounded-lg relative flex-grow mr-8 placeholder:text-indigo-400 border-transparent"
          type="search"
          placeholder={`${windowSize.width > 540 ? placeholder : ""}`}
          value={term}
          onChange={onChange}
        />
        <div className="rounded-lg absolute inset-0 shadow-innerThin z-0 pointer-events-none" />
        {term.length > 0 && (
          <div data-cy="search-clear-button" className="flex items-center mx-2 text-indigo-400 shrink-0 absolute top-0 right-0 mr-16 h-full md:mr-20 z-20">
            <Close onClick={clearSearch} size="16" />
          </div>
        )}
        <div className="flex items-center justify-end">
          <SearchButton onClick={() => handleSearchInput(term)} />
        </div>
        <SearchDropdown term={term} show={formFocus} handleSearchClick={handleSuggestionClick} />
      </div>
    </form>
  );
};
export default SearchForm;
