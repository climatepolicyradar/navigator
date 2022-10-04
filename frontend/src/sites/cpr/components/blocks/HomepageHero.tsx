import { FC } from "react";
import { useTranslation } from "react-i18next";
import { Hero } from "@components/blocks/Hero";
import LandingSearchForm from "@components/forms/LandingSearchForm";
import AlphaLogo from "@components/logo/AlphaLogo";
import ExactMatch from "@components/filters/ExactMatch";
import LandingPageLinks from "@components/blocks/LandingPageLinks";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  handleSearchChange: (type: string, value: any) => void;
  searchInput: string;
  exactMatch: boolean;
};

const HomepageHero = ({ handleSearchInput, handleSearchChange, searchInput, exactMatch }: TProps) => {
  const { t } = useTranslation(["searchStart", "searchResults"]);

  const handleLinkClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const term = e.currentTarget.textContent;
    handleSearchInput(term);
  };

  return (
    <Hero>
      <AlphaLogo />
      <div className="container mt-24 md:mt-48 max-w-screen-lg mx-auto">
        <LandingSearchForm handleSearchInput={handleSearchInput} placeholder={t("Search for something, e.g. 'carbon taxes'")} input={searchInput} />
        <div className="mt-4 flex justify-end">
          <ExactMatch landing={true} checked={exactMatch} id="exact-match" handleSearchChange={handleSearchChange} />
        </div>
        <div className="mt-12">
          <LandingPageLinks handleLinkClick={handleLinkClick} />
        </div>
      </div>
    </Hero>
  );
};

export default HomepageHero;
