import { useRouter } from "next/router";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import useSearchCriteria from "@hooks/useSearchCriteria";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useUpdateSearch from "@hooks/useUpdateSearch";
import useUpdateCountries from "@hooks/useUpdateCountries";
import Layout from "@components/layouts/LandingPage";
import LoaderOverlay from "@components/LoaderOverlay";
import { initialSearchCriteria } from "@constants/searchCriteria";
import { emptySearchResults } from "@constants/search";
import useConfig from "@hooks/useConfig";
import getSite from "@utils/getSite";

import CPRHomepage from "@cpr/components/blocks/HomepageHero";

const IndexPage = () => {
  const { t, ready } = useTranslation(["searchStart", "searchResults"]);
  const router = useRouter();
  const { data: searchCriteria }: any = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const { mutate: updateCountries } = useUpdateCountries();
  const { mutate: updateSearch } = useUpdateSearch();
  const site = getSite();

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

  if (!ready || !searchCriteria) return <LoaderOverlay />;

  return (
    <>
      <Layout title={t("Law and Policy Search")}>
        {site === "cpr" && (
          <CPRHomepage
            handleSearchInput={handleSearchInput}
            handleSearchChange={handleSearchChange}
            searchInput={searchCriteria.query_string}
            exactMatch={searchCriteria.exact_match}
          />
        )}
        {site === "cclw" && null}
      </Layout>
    </>
  );
};

export default IndexPage;
