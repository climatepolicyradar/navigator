import { useState, useEffect, useRef } from 'react';
import Close from '../buttons/Close';
import useWindowResize from '../../hooks/useWindowResize';
import { SearchIcon } from '../Icons';
import { StartTextAnimation } from '../../utils/typewriter';

interface SearchFormProps {
  placeholder: string;
  handleSearchInput(e: any, term: string);
  input?: string;
}

const LandingSearchForm = ({ input, handleSearchInput }: SearchFormProps) => {
  const [term, setTerm] = useState('');
  const windowSize = useWindowResize();
  const inputRef = useRef(null);

  const typePlaceholder = () => {
    const text = ['Search full text of 1032 laws and policies'];
    StartTextAnimation(0, text, inputRef.current);
  };
  const clearSearch = (e) => {
    e.preventDefault();
    setTerm('');
  };
  const clearPlaceholder = () => {
    inputRef.current.placeholder = '';
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
  return (
    <form data-cy="search-form">
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
          <div
            data-cy="search-clear-button"
            className="flex text-indigo-300 items-center mx-2 shrink-0 absolute top-0 right-0 mr-20 h-full z-20 h-full items-center"
          >
            <Close onClick={clearSearch} size="16" />
          </div>
        )}
        <button
          className="absolute top-0 right-0 -mt-1"
          onClick={(e) => handleSearchInput(e, term)}
        >
          <SearchIcon height="40" width="80" />
        </button>
      </div>
      {/* <div className="relative shadow-md rounded-lg bg-white flex items-stretch">
        <input
          data-cy="search-input"
          className="bg-transparent text-indigo-600 appearance-none py-2 pl-2 z-10 rounded-lg relative flex-grow mr-8 placeholder:text-indigo-400 border-transparent"
          type="search"
          placeholder={`${windowSize.width > 540 ? placeholder : ''}`}
          value={term}
          onChange={onChange}
        />
        <div className="rounded-lg absolute inset-0 shadow-innerThin z-0 pointer-events-none" />
        {term.length > 0 && (
          <div
            data-cy="search-clear-button"
            className="flex items-center mx-2 text-indigo-400 shrink-0 absolute top-0 right-0 mr-16 h-full md:mr-20 z-20 h-full items-center"
          >
            <Close onClick={clearSearch} size="16" />
          </div>
        )}
        <div className="flex items-center justify-end">
          <SearchButton onClick={(e) => handleSearchInput(e, term)} />
        </div>
      </div> */}
    </form>
  );
};
export default LandingSearchForm;
