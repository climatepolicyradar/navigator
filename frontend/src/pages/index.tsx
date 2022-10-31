import { useRouter } from "next/router";
import React, { useEffect, useContext } from "react";
import { useTranslation } from "react-i18next";
import useSearchCriteria from "@hooks/useSearchCriteria";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useUpdateSearch from "@hooks/useUpdateSearch";
import useUpdateCountries from "@hooks/useUpdateCountries";
import useConfig from "@hooks/useConfig";
import Layout from "@components/layouts/LandingPage";
import { initialSearchCriteria } from "@constants/searchCriteria";
import { emptySearchResults } from "@constants/search";

import CPRLandingPage from "@cpr/pages/landing-page";
import CCLWLandingPage from "@cclw/pages/landing-page";

import { ThemeContext } from "@context/ThemeContext";

const IndexPage = () => {
  const { t } = useTranslation(["searchStart", "searchResults"]);
  const router = useRouter();
  const { data: searchCriteria }: any = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const { mutate: updateCountries } = useUpdateCountries();
  const { mutate: updateSearch } = useUpdateSearch();
  const theme = useContext(ThemeContext);

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
    updateSearchCriteria.mutate({ ...initialSearchCriteria, ...newSearchCritera, ...additionalCritera });
    router.push("/search");
  };

  const handleSearchChange = (type: string, value: any) => {
    updateSearchCriteria.mutate({ [type]: value });
  };

  useEffect(() => {
    updateCountries({
      regionName: "",
      regions,
      countries,
    });
    updateSearch({ data: emptySearchResults });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [updateCountries, updateSearch]);

  return (
    <>
      <Layout title={t("Law and Policy Search")}>
        {theme === "cpr" && (
          <CPRLandingPage
            handleSearchInput={handleSearchInput}
            handleSearchChange={handleSearchChange}
            searchInput={searchCriteria?.query_string ?? ""}
            exactMatch={searchCriteria?.exact_match ?? false}
          />
        )}
        {theme === "cclw" && <CCLWLandingPage handleSearchInput={handleSearchInput} searchInput={searchCriteria?.query_string ?? ""} />}
      </Layout>
    </>
  );
};

export default IndexPage;
