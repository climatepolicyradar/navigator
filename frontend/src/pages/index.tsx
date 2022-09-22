import { useRouter } from "next/router";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import useSearchCriteria from "@hooks/useSearchCriteria";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useUpdateSearch from "@hooks/useUpdateSearch";
import useUpdateCountries from "@hooks/useUpdateCountries";
import Layout from "@components/layouts/LandingPage";
import { Hero } from "@components/blocks/Hero";
import LoaderOverlay from "@components/LoaderOverlay";
import LandingSearchForm from "@components/forms/LandingSearchForm";
import AlphaLogo from "@components/logo/AlphaLogo";
import ExactMatch from "@components/filters/ExactMatch";
import LandingPageLinks from "@components/blocks/LandingPageLinks";
import { initialSearchCriteria } from "@constants/searchCriteria";
import { emptySearchResults } from "@constants/search";
import useConfig from "@hooks/useConfig";

const IndexPage = () => {
  const { t, ready } = useTranslation(["searchStart", "searchResults"]);
  const router = useRouter();
  const { data: searchCriteria }: any = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateCountries = useUpdateCountries();
  const updateSearch = useUpdateSearch();

  const configQuery: any = useConfig("config");
  const { data: { regions = [], countries = [] } = {} } = configQuery;

  const handleSearchInput = (term: string, filter?: string, filterValue?: string) => {
    const newSearchCritera = {
      ["query_string"]: term,
    };
    let additionalCritera = {};
    if (filter && filterValue && filter.length && filterValue.length) {
      additionalCritera = { ...additionalCritera, ["keyword_filters"]: { [filter]: [filterValue] } };
    }
    updateSearchCriteria.mutate({ ...newSearchCritera, ...additionalCritera });
    router.push("/search");
  };

  const handleSearchChange = (type: string, value: any) => {
    updateSearchCriteria.mutate({ [type]: value });
  };

  const handleLinkClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const term = e.currentTarget.textContent;
    handleSearchInput(term);
  };

  const clearAllFilters = () => {
    /*
    clear all previously set filters if returning from
    a previous search
    */
    const { query_string, ...initial } = initialSearchCriteria;
    updateSearchCriteria.mutate(initial);
    // reset filtered countries which show in suggest list
    // when typing in a jurisdiction/country
    updateCountries.mutate({
      regionName: "",
      regions,
      countries,
    });
  };

  const clearSearch = () => {
    updateSearch.mutate({ data: emptySearchResults });
  };

  useEffect(() => {
    clearAllFilters();
    clearSearch();
  }, []);

  return (
    <>
      {!ready || !searchCriteria ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Climate Policy Radar | ${t("Law and Policy Search")}`}>
          <Hero>
            <AlphaLogo />
            <div className="container mt-24 md:mt-48 max-w-screen-lg mx-auto">
              <LandingSearchForm handleSearchInput={handleSearchInput} placeholder={t("Search for something, e.g. 'carbon taxes'")} input={searchCriteria.query_string} />
              <div className="mt-4 flex justify-end">
                <ExactMatch landing={true} checked={searchCriteria.exact_match} id="exact-match" handleSearchChange={handleSearchChange} />
              </div>
              <div className="mt-12">
                <LandingPageLinks handleLinkClick={handleLinkClick} />
              </div>
            </div>
          </Hero>
        </Layout>
      )}
    </>
  );
};

export default IndexPage;
