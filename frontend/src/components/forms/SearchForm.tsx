import React, { useState, useEffect } from "react";
import Close from "../buttons/Close";
import SearchButton from "../buttons/SearchButton";
import useWindowResize from "../../hooks/useWindowResize";

interface SearchFormProps {
  placeholder: string;
  handleSearchInput(term: string): void;
  input?: string;
}

const SearchForm = ({ input, placeholder, handleSearchInput }: SearchFormProps) => {
  const [term, setTerm] = useState("");
  const windowSize = useWindowResize();

  const clearSearch = () => {
    setTerm("");
  };

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTerm(e.currentTarget.value);
  };

  useEffect(() => {
    if (input) setTerm(input);
  }, [input]);

  return (
    <form data-cy="search-form">
      <div className="relative shadow-md rounded-lg bg-white flex items-stretch z-0">
        <input
          data-cy="search-input"
          className="bg-transparent text-indigo-600 appearance-none py-2 pl-2 z-10 rounded-lg relative flex-grow mr-8 placeholder:text-indigo-400 border-transparent"
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
      </div>
    </form>
  );
};
export default SearchForm;
