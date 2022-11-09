import { useEffect, useState } from "react";
import SuggestList from "./SuggestList";
import { useTranslation } from "react-i18next";
import { sortData } from "@utils/sorting";

interface ByTextInputProps {
  title: string;
  list: Object[];
  selectedList: string[];
  keyField: string;
  keyFieldDisplay?: string;
  filterType: string;
  handleFilterChange(filterType: string, value: string, action?: string): void;
}

const ByTextInput = ({ title, list, selectedList, keyField, keyFieldDisplay, filterType, handleFilterChange }: ByTextInputProps) => {
  const [input, setInput] = useState("");
  const [suggestList, setSuggestList] = useState([]);
  const { t } = useTranslation("searchResults");

  const handleChange = (e: React.FormEvent<HTMLInputElement>): void => {
    setInput(e.currentTarget.value);
  };

  useEffect(() => {
    if (!input.length) {
      setSuggestList([]);
      return;
    }
    const filteredList = list?.filter((item) => {
      /* Make sure item hasn't already been selected and limit list to 20 items */
      return item[keyFieldDisplay ?? keyField].toLowerCase().indexOf(input.toLowerCase()) > -1 && selectedList.indexOf(item[keyField]) === -1;
    });
    setSuggestList(sortData(filteredList, keyField));
  }, [input, keyField, keyFieldDisplay, list, selectedList]);

  return (
    <div className="relative">
      <div>{title}</div>
      <input
        type="text"
        className="border border-indigo-200 mt-2 small outline-none placeholder:text-indigo-300"
        placeholder={t("Start typing")}
        value={input}
        onChange={handleChange}
      />

      {suggestList.length > 0 && (
        <div className="absolute top-3 mt-12 left-0 w-full z-30">
          <SuggestList list={suggestList} setList={setSuggestList} keyField={keyField} keyFieldDisplay={keyFieldDisplay} type={filterType} setInput={setInput} handleFilterChange={handleFilterChange} />
        </div>
      )}
    </div>
  );
};
export default ByTextInput;
