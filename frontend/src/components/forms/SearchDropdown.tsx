import { useRouter } from "next/router";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useConfig from "@hooks/useConfig";
import { TGeography } from "@types";
import { SearchIcon } from "@components/svg/Icons";

type TProps = {
  show: boolean;
  term: string;
  handleSearchClick: (term: string, filter?: string, filterValue?: string) => void;
  largeSpacing?: boolean;
};

export const SearchDropdown = ({ show = false, term, handleSearchClick, largeSpacing }: TProps) => {
  const updateSearchCriteria = useUpdateSearchCriteria();
  const router = useRouter();
  const configQuery: any = useConfig("config");
  const geographies: TGeography[] = configQuery.data?.countries || [];

  const geographiesFiltered = geographies.filter(
    (geography: TGeography) => geography.display_value.toLowerCase().includes(term.toLocaleLowerCase()) || term.toLocaleLowerCase().includes(geography.display_value.toLowerCase())
  );

  const termWithoutGeography = (geography: string) => term.toLowerCase().replace(geography.toLowerCase(), "").trim();

  if (!term || !show) return null;

  const handleClick = (e: any) => {
    e.preventDefault();
    handleSearchClick(term);
  };

  const handleCountryClick = (e: React.MouseEvent<HTMLAnchorElement>, url: string) => {
    e.preventDefault();
    updateSearchCriteria.mutate({ ["query_string"]: term });
    router.push(url);
  };

  const handleSuggestionClick = (e: React.MouseEvent<HTMLAnchorElement>, geography: string) => {
    e.preventDefault();
    handleSearchClick(termWithoutGeography(geography), "countries", geography);
  };

  const anchorClasses = (last: boolean) => `flex items-center cursor-pointer py-2 px-4 block hover:bg-blue-200 focus:bg-blue-200 ${last ? "rounded-b-lg" : ""}`;

  const renderSearchSuggestion = (geography: string) => {
    if (!term.toLowerCase().includes(geography.toLowerCase())) return;
    if (!termWithoutGeography(geography).trim().length) return;
    return (
      <ul>
        <li key={geography}>
          <a href="#" className={anchorClasses(false)} onClick={(e) => handleSuggestionClick(e, geography)}>
            Did you mean to search for <span className="font-bold text-black mx-2">{term.toLowerCase().replace(geography.toLowerCase(), "")}</span> in{" "}
            <span className="font-bold text-black ml-2">{geography}</span>?
          </a>
        </li>
      </ul>
    );
  };

  return (
    <div className={`absolute bg-blue-100 w-full text-indigo-400 rounded-b-lg max-h-[300px] overflow-y-auto search-dropdown ${largeSpacing ? "search-dropdown_large" : ""}`}>
      <a href="#" className={anchorClasses(!geographiesFiltered.length)} onClick={handleClick}>
        <span className="mr-2 w-[20px]">
          <SearchIcon />
        </span>
        Search <span className="font-bold text-black mx-1">{term}</span> in all documents
      </a>
      {geographiesFiltered.length === 1 && renderSearchSuggestion(geographiesFiltered[0].display_value)}
      {!!geographiesFiltered.length && (
        <>
          <div className="py-2 px-4 text-sm mt-2">View countries and territories information</div>
          <ul>
            {geographiesFiltered.map((geography, i) => {
              const last = i + 1 === geographiesFiltered.length;
              return (
                <li key={geography.id}>
                  <a href="#" className={anchorClasses(last)} onClick={(e) => handleCountryClick(e, `/geography/${geography.id}`)}>
                    <span className="font-bold text-black">{geography.display_value}</span> <span className="text-sm ml-4">Geography profile</span>
                  </a>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
};
