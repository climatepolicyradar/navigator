import { useState, useEffect } from 'react';
import Close from '../buttons/Close';
import SearchButton from '../buttons/SearchButton';
import useWindowResize from '../../hooks/useWindowResize';

interface SearchFormProps {
  placeholder: string;
  handleSearchChange(type: string, value: string): void;
}

const SearchForm = ({ placeholder, handleSearchChange }: SearchFormProps) => {
  const [term, setTerm] = useState('');
  const windowSize = useWindowResize();
  const onClick = (e) => {
    e.preventDefault();
    setTerm('');
  };
  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };
  const handleSearch = (e) => {
    e.preventDefault();
    handleSearchChange('query_string', term);
  };
  return (
    <form data-cy="search-form">
      <div className="relative shadow-md rounded-lg bg-white flex items-stretch">
        <input
          data-cy="search-input"
          className="bg-transparent text-indigo-600 appearance-none py-2 pl-2 z-10 rounded-lg relative flex-grow mr-8 placeholder:text-indigo-400"
          type="search"
          placeholder={`${windowSize.width > 540 ? placeholder : ''}`}
          value={term}
          onChange={onChange}
        />
        <div className="rounded-lg absolute inset-0 border border-indigo-200 z-0" />
        {term.length > 0 && (
          <div
            data-cy="search-clear-button"
            className="flex items-center mx-2 text-indigo-400 shrink-0 absolute top-0 right-0 mr-16 h-full md:mr-20 z-20 h-full items-center"
          >
            <Close onClick={onClick} size="16" />
          </div>
        )}
        <div className="flex items-center justify-end z-10">
          <SearchButton onClick={handleSearch} />
        </div>
      </div>
    </form>
  );
};
export default SearchForm;
