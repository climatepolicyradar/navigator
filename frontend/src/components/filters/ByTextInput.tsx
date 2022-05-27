import { useEffect, useState } from 'react';
import SuggestList from './SuggestList';
import '../../pages/i18n';
import { useTranslation } from 'react-i18next';

interface ByTextInputProps {
  title: string;
  list: Object[];
  selectedList: string[];
  keyField: string;
  filterType: string;
  handleFilterChange(filterType: string, value: string): void;
}

const ByTextInput = ({
  title,
  list,
  selectedList,
  keyField,
  filterType,
  handleFilterChange,
}: ByTextInputProps) => {
  const [input, setInput] = useState('');
  const [suggestList, setSuggestList] = useState([]);
  const { t, i18n, ready } = useTranslation('searchResults');
  const handleChange = (e: React.FormEvent<HTMLInputElement>): void => {
    setInput(e.currentTarget.value);
  };
  const suggest = (input: string): void => {
    if (!input.length) {
      setSuggestList([]);
      return;
    }
    const filteredList = list.filter((item) => {
      /* Make sure item hasn't already been selected and limit list to 20 items */
      return (
        item[keyField].toLowerCase().indexOf(input.toLowerCase()) > -1 &&
        selectedList.indexOf(item[keyField]) === -1
      );
    });
    setSuggestList(filteredList);
  };
  useEffect(() => {
    suggest(input);
  }, [input]);
  return (
    <div className="relative">
      <div>{title}</div>
      <input
        type="text"
        className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        placeholder={t('Start typing')}
        value={input}
        onChange={handleChange}
      />

      {suggestList.length > 0 && (
        <div className="absolute top-3 mt-12 left-0 w-full z-30">
          <SuggestList
            list={suggestList}
            setList={setSuggestList}
            keyField={keyField}
            type={filterType}
            setInput={setInput}
            handleFilterChange={handleFilterChange}
          />
        </div>
      )}
    </div>
  );
};
export default ByTextInput;
