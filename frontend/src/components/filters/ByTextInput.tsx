import { useEffect, useState } from 'react';
import SuggestList from './SuggestList';
import '../../pages/i18n';
import { useTranslation } from 'react-i18next';

interface ByTextInputProps {
  title: string;
  list: Object[];
  keyField: string;
  type: string;
  handleFilterChange(type: string, value: string): void;
}

const ByTextInput = ({
  title,
  list,
  keyField,
  type,
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
      /* TODO: Make sure item hasn't already been selected */
      return item[keyField].toLowerCase().indexOf(input.toLowerCase()) > -1;
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
        className="border border-indigo-200 mt-2 small outline-none"
        placeholder={t('Start typing')}
        value={input}
        onChange={handleChange}
      />
      {/* TODO: add clickable tags for each item that is added (click x to remove) */}
      {suggestList.length > 0 && (
        <div className="absolute top-3 mt-12 left-0 w-full z-20">
          <SuggestList
            list={suggestList}
            setList={setSuggestList}
            keyField={keyField}
            type={type}
            setInput={setInput}
            onClick={handleFilterChange}
          />
        </div>
      )}
    </div>
  );
};
export default ByTextInput;
