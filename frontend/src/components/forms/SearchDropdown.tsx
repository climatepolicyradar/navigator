import Link from "next/link";
import { useRouter } from "next/router";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useNestedLookups from "@hooks/useNestedLookups";
import { TGeography } from "@types";
import { SearchIcon } from "@components/svg/Icons";

type TProps = {
  show: boolean;
  term: string;
  handleSearchClick: () => void;
};

export const SearchDropdown = ({ show = false, term, handleSearchClick }: TProps) => {
  const updateSearchCriteria = useUpdateSearchCriteria();
  const router = useRouter();
  const geosQuery: any = useNestedLookups("geographies", "", 2);
  const geographies: TGeography[] = geosQuery.data?.data?.level2 || [];

  const geographiesFiltered = geographies.filter(
    (geography: TGeography) => geography.display_value.toLowerCase().includes(term.toLocaleLowerCase()) || geography.value.toLowerCase().includes(term.toLowerCase())
  );

  if (!term || !show) return null;

  const handleClick = (e: any) => {
    e.preventDefault();
    handleSearchClick();
  };

  const handleCountryClick = (e: React.MouseEvent<HTMLAnchorElement>, url: string) => {
    e.preventDefault();
    updateSearchCriteria.mutate({ ["query_string"]: term });
    router.push(url);
  };

  const anchorClasses = (last: boolean) => `flex items-center cursor-pointer py-2 px-4 block hover:bg-blue-200 focus:bg-blue-200 ${last ? "rounded-b-lg" : ""}`;

  return (
    <div className="absolute top-[50px] bg-blue-100 w-full text-indigo-400 rounded-b-lg max-h-[300px] overflow-y-auto">
      <a href="#" className={anchorClasses(!geographiesFiltered.length)} onClick={handleClick}>
        <span className="mr-2 w-[20px]">
          <SearchIcon />
        </span>
        Search <span className="font-bold text-black mx-1">{term}</span> in all documents
      </a>
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
