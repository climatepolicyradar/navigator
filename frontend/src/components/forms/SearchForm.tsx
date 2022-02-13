import { useState } from 'react';
import Close from '../buttons/Close';
import SearchButton from '../buttons/SearchButton';
import { SearchIcon } from '../Icons';

const SearchForm = () => {
  const [term, setTerm] = useState('');
  const onClick = (e) => {
    e.preventDefault();
    setTerm('');
  };
  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };
  return (
    <form>
      <div className="mt-8 md:mt-16 bg-white p-2 pl-3 rounded-full text-indigo-300 flex">
        <SearchIcon height="40" width="40" />
        <input
          className="md:text-xl w-full mx-2 px-2 text-indigo-600 appearance-none focus:outline-indigo-500 focus:outline-dashed rounded-full"
          type="search"
          placeholder="Search for something, e.g. 'carbon taxes'"
          value={term}
          onChange={onChange}
        />
        {term.length > 0 && (
          <div className="flex items-center mx-2 text-indigo-500 shrink-0">
            <Close onClick={onClick} size="30" />
          </div>
        )}

        <SearchButton>GO</SearchButton>
      </div>
    </form>
  );
};
export default SearchForm;
