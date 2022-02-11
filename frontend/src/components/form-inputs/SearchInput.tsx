import SearchButton from '../buttons/SearchButton';
import { SearchIcon } from '../Icons';

const SearchInput = () => {
  return (
    <div className="mt-16 bg-white p-2 pl-3 rounded-full text-indigo-300 flex">
      <SearchIcon height="40" width="40" />
      <input
        className="text-xl w-full pl-2 text-indigo-600"
        type="search"
        placeholder="Search for something, e.g. 'carbon taxes'"
      />
      <SearchButton>GO</SearchButton>
    </div>
  );
};
export default SearchInput;
