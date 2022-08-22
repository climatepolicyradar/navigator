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
  const countries: TGeography[] = geosQuery.data?.data?.level2 || [];

  const countriesFiltered = countries.filter(
    (country: TGeography) => country.display_value.toLowerCase().includes(term.toLocaleLowerCase()) || country.value.toLowerCase().includes(term.toLowerCase())
  );

  if (!term || !show) return null;

  const handleClick = (e: any) => {
    e.preventDefault();
    handleSearchClick();
  };

  const handleCountryClick = (url: string) => {
    updateSearchCriteria.mutate({ ["query_string"]: term });
    router.push(url);
  };

  const anchorClasses = (last: boolean) => `flex items-center cursor-pointer py-2 px-4 block hover:bg-blue-200 ${last ? "rounded-b-lg" : ""}`;

  return (
    <div className="absolute top-[50px] bg-blue-100 w-full text-indigo-400 rounded-b-lg max-h-[300px] overflow-y-auto">
      <a href="#" className={anchorClasses(!countriesFiltered.length)} onClick={handleClick}>
        <span className="mr-2 w-[20px]">
          <SearchIcon />
        </span>
        Search <span className="font-bold text-black mx-1">{term}</span> in all documents
      </a>
      {!!countriesFiltered.length && (
        <>
          <div className="py-2 px-4 text-sm mt-2">View countries and territories information</div>
          <ul>
            {countriesFiltered.map((country, i) => {
              const last = i + 1 === countriesFiltered.length;
              return (
                <li className={anchorClasses(last)} key={country.id} onClick={() => handleCountryClick(`/country/${country.id}`)}>
                  <span className="font-bold text-black">{country.display_value}</span> <span className="text-sm ml-4">Country profile</span>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </div>
  );
};
