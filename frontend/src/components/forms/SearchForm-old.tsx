import { useState, useEffect } from 'react';
import Close from '../buttons/Close';
import SearchButton from '../buttons/SearchButton';
import { SearchIcon } from '../svg/Icons';
import useWindowResize from '../../hooks/useWindowResize';

interface SearchFormProps {
  placeholder: string;
  buttonText: string;
}

const SearchForm = ({ placeholder, buttonText }: SearchFormProps) => {
  const [term, setTerm] = useState('');
  const windowSize = useWindowResize();
  const onClick = (e) => {
    e.preventDefault();
    setTerm('');
  };
  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };
  return (
    <form data-cy="search-form">
      <p className="sm:hidden mt-4 text-center text-white">{placeholder}</p>
      <div className="mt-4 md:mt-16 relative">
        <div className="absolute top-0 left-0 ml-4 mt-3 text-indigo-400 z-20">
          <SearchIcon height="35" width="40" />
        </div>

        <input
          data-cy="search-input"
          className="md:text-xl w-full mx-2 text-indigo-600 appearance-none bg-white py-4 pl-12 pr-28 md:pl-16 md:pr-40 rounded-full flex rounded-full relative z-10"
          type="search"
          placeholder={`${windowSize.width > 540 ? placeholder : ''}`}
          value={term}
          onChange={onChange}
        />
        {term.length > 0 && (
          <div
            data-cy="search-clear-button"
            className="flex items-center mx-2 text-indigo-500 shrink-0 absolute top-0 right-0 mr-16 pr-1 md:mr-28 z-20 h-full items-center"
          >
            <Close onClick={onClick} size="30" />
          </div>
        )}
        <div className="absolute top-0 right-0 md:mr-1 h-full flex items-center justify-end z-10">
          <SearchButton>{buttonText}</SearchButton>
        </div>
      </div>
    </form>
  );
};
export default SearchForm;
