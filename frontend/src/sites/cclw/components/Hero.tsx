import LandingSearchForm from "@components/forms/LandingSearchForm";
import Button from "@components/buttons/Button";
import { ExternalLink } from "@components/ExternalLink";

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
    <div className="pt-12 pb-6 text-white">
      <div className="container">
        <div className="mx-auto text-center">
          <p className="text-lg lg:text-2xl">Use our database to search climate laws and policies globally</p>
        </div>
        <div className="max-w-screen-lg mx-auto mt-6">
          <LandingSearchForm handleSearchInput={handleSearchInput} placeholder="Search for countries, legislation and policies and litigation cases" input={searchInput} />
        </div>
        <div className="mt-6 lg:mt-12 grid gap-y-5 gap-x-8 sm:grid-cols-1 lg:grid-cols-3 text-center max-w-screen-lg mx-auto">
          <div className="lg:px-8 flex flex-col items-center">
            <div className="text-lg font-bold">Laws and policies</div>
            <a className="cclw-semi-circle" href="#" onClick={(e) => handleDocumentBrowseClick(e, "Policy")}>
              <span className="block">
                Browse
                <span className="font-bold"> 2,576</span>
              </span>
              <span className="block">
                laws & policies
                <span className="font-bold"> &gt;</span>
              </span>
            </a>
          </div>
          <div className="border-y lg:border-y-0 lg:border-x border-white py-5 lg:py-0 lg:px-8">
            <div className="text-lg font-bold">Litigation</div>
            {/* <div className="flex items-center justify-center my-4 cursor-pointer hover:underline" role="button" onClick={(e) => handleDocumentBrowseClick(e, "Law")}>
              <div className="p-3 border bg-secondary-500 border-overlayWhite rounded-full mr-[-5px]">{getCategoryIcon("Case")}</div>
              <div className="w-[100px] h-[100px] bg-primary-400 rounded-full text-3xl flex items-center justify-center">2,082</div>
            </div> */}
            <div className="mt-6">
              <p>Climate litigation is coming soon</p>
              <ExternalLink url="https://climatepolicyradar.org/latest" className="font-bold underline">
                Read more &gt;
              </ExternalLink>
            </div>
            <div className="mt-6">
              <p>
                Climate Change Litigation data currently available at{" "}
                <ExternalLink url="http://climatecasechart.com/" className="font-bold underline">
                  climatecasechart.com
                </ExternalLink>
              </p>
            </div>
          </div>
          <div className="flex flex-col justify-between items-center lg:px-8">
            <div className="text-lg font-bold">Technology</div>
            <div className="mt-4">We are now powered by data science and AI.</div>
            <div className="mt-4">
              <ExternalLink url="https://climatepolicyradar.org/what-we-do">
                <Button extraClasses="flex items-center">
                  <span>Learn more about our technology</span>
                  <span className="text-3xl ml-4">&gt;</span>
                </Button>
              </ExternalLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
