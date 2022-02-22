import { useState, useEffect } from 'react';
import Close from '../buttons/Close';
import SearchButton from '../buttons/SearchButton';
import { SearchIcon } from '../Icons';
import useWindowResize from '../hooks/useWindowResize';
import { useTranslation } from 'react-i18next';

const SearchForm = () => {
  const [term, setTerm] = useState('');
  const windowSize = useWindowResize();
  const { t, i18n } = useTranslation();
  const onClick = (e) => {
    e.preventDefault();
    setTerm('');
  };
  const onChange = (e) => {
    setTerm(e.currentTarget.value);
  };
  return (
    <form>
      <div>{t('description.part2')}</div>
      <p className="sm:hidden mt-4 text-center text-white">
        Search for something, e.g. 'carbon taxes'.
      </p>
      <div className="mt-4 md:mt-16 relative">
        <div className="absolute top-0 left-0 ml-4 mt-3 text-indigo-400 z-20">
          <SearchIcon height="35" width="40" />
        </div>

        <input
          className="md:text-xl w-full mx-2 text-indigo-600 appearance-none bg-white py-4 pl-12 pr-28 md:pl-16 md:pr-40 rounded-full flex rounded-full relative z-10"
          type="search"
          placeholder={`${
            windowSize.width > 540
              ? "Search for something, e.g. 'carbon taxes'"
              : ''
          }`}
          value={term}
          onChange={onChange}
        />
        {term.length > 0 && (
          <div className="flex items-center mx-2 text-indigo-500 shrink-0 absolute top-0 right-0 mr-16 pr-1 md:mr-28 z-20 h-full items-center">
            <Close onClick={onClick} size="30" />
          </div>
        )}
        <div className="absolute top-0 right-0 md:mr-1 h-full flex items-center justify-end z-10">
          <SearchButton>GO</SearchButton>
        </div>
      </div>
    </form>
  );
};
export default SearchForm;
