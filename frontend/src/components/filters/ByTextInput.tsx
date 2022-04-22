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
      return item[keyField].toLowerCase().indexOf(input.toLowerCase()) > -1;
    });
    setSuggestList(filteredList);
  };
  useEffect(() => {
    suggest(input);
  }, [input]);
  return (
    <div>
      <div>{title}</div>
      <input
        type="text"
        className="border border-indigo-200 mt-2 small"
        placeholder={t('Start typing')}
        value={input}
        onChange={handleChange}
      />
      {suggestList.length > 0 && (
        <SuggestList
          list={suggestList}
          setList={setSuggestList}
          keyField={keyField}
          type={type}
          setInput={setInput}
          onClick={handleFilterChange}
        />
      )}
    </div>
  );
};
export default ByTextInput;

/*
What we need:
Title (props)
type?
Suggest list - updates as user types in
Selected list (filters)

*/
