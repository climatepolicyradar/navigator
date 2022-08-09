import { useState, useEffect, useRef } from 'react';
import Close from '../buttons/Close';
import useWindowResize from '@hooks/useWindowResize';
import { SearchIcon } from '../svg/Icons';
import { StartTextAnimation } from '@utils/typewriter';

interface SearchFormProps {
  placeholder: string;
  handleSearchInput(e: any, term: string);
  input?: string;
}

function LandingSearchForm({ input, handleSearchInput }: SearchFormProps) {
  const [term, setTerm] = useState('');
  const windowSize = useWindowResize();
  const inputRef = useRef(null);

  const typePlaceholder = () => {
    const text = ['Search full text of 3000+ laws and policies'];
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
            className="flex text-indigo-300 mx-2 shrink-0 absolute top-0 right-0 mr-20 h-full z-20 items-center"
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
    </form>
  );
}
export default LandingSearchForm;
