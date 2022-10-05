import LandingSearchForm from "@components/forms/LandingSearchForm";
import { CountryLink } from "@components/CountryLink";
import { getCategoryIcon } from "@helpers/getCatgeoryIcon";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  searchInput: string;
};

export const Hero = ({ handleSearchInput, searchInput }: TProps) => {
  const handleDocumentBrowseClick = (e: React.MouseEvent, category: string) => {
    e.preventDefault();
    handleSearchInput("", "categories", category);
  };

  return (
    <div className="bg-secondary-700 pt-4 pb-12 text-white">
      <div className="container">
        <h1 className="text-primary-400 text-center my-4">Climate Change Laws of the World</h1>
        <div className="max-w-screen-sm mx-auto text-center">
          <p className="text-lg">Use our database to search and browse climate laws, policies and ligitation cases globally</p>
        </div>
        <div className="max-w-screen-lg mx-auto mt-6">
          <LandingSearchForm handleSearchInput={handleSearchInput} placeholder="Search for countries, legislation and policies and litigation cases" input={searchInput} />
        </div>
        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 text-center">
          <div>
            <div className="text-lg font-bold">Climate laws and policies</div>
            <div className="flex items-center justify-center my-4 cursor-pointer hover:underline" role="button" onClick={(e) => handleDocumentBrowseClick(e, "Policy")}>
              <div className="p-3 border bg-secondary-500 border-overlayWhite rounded-full mr-[-5px]">{getCategoryIcon("Law")}</div>
              <div className="w-[100px] h-[100px] bg-primary-400 rounded-full text-3xl flex items-center justify-center">2,576</div>
            </div>
            <a className="cursor-pointer hover:underline" onClick={(e) => handleDocumentBrowseClick(e, "Policy")}>
              Search laws and policy &gt;
            </a>
          </div>
          <div>
            <div className="text-lg font-bold">Climate litigation cases</div>
            <div className="flex items-center justify-center my-4 cursor-pointer hover:underline" role="button" onClick={(e) => handleDocumentBrowseClick(e, "Law")}>
              <div className="p-3 border bg-secondary-500 border-overlayWhite rounded-full mr-[-5px]">{getCategoryIcon("Case")}</div>
              <div className="w-[100px] h-[100px] bg-primary-400 rounded-full text-3xl flex items-center justify-center">2,082</div>
            </div>
            <a className="cursor-pointer hover:underline" href="#" onClick={(e) => handleDocumentBrowseClick(e, "Law")}>
              Search litigation cases &gt;
            </a>
          </div>
          <div>
            <div className="text-lg font-bold">Country profiles</div>
            <div className="mt-4">View all legislation, policies and litigation cases in a country.</div>
            <div className="mt-4">
              <div className="font-bold">Featured:</div>
              <div className="flex gap-4 mt-2 justify-center text-white text-sm">
                <CountryLink countryCode="KOR" className="hover:text-primary-400">
                  <span className={`rounded-sm border border-black flag-icon-background flag-icon-kor`} />
                  <span className="ml-2">South Korea</span>
                </CountryLink>
                <CountryLink countryCode="BRA" className="hover:text-primary-400">
                  <span className={`rounded-sm border border-black flag-icon-background flag-icon-bra`} />
                  <span className="ml-2">Brazil</span>
                </CountryLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
