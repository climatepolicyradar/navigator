import { useRouter } from 'next/router';
import { useEffect } from 'react';
import Layout from '../components/layouts/LandingPage';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import { useAuth } from '../api/auth';
import useSearchCriteria from '../hooks/useSearchCriteria';
import useUpdateSearchCriteria from '../hooks/useUpdateSearchCriteria';
import LandingSearchForm from '../components/forms/LandingSearchForm';
import AlphaLogo from '../components/logo/AlphaLogo';
import ExactMatch from '../components/filters/ExactMatch';
import LandingPageLinks from '../components/blocks/LandingPageLinks';
import { initialSearchCriteria } from '../constants/searchCriteria';
import { emptySearchResults } from '../constants/search';
import useUpdateSearch from '../hooks/useUpdateSearch';
import useNestedLookups from '../hooks/useNestedLookups';
import useUpdateCountries from '../hooks/useUpdateCountries';
import Tooltip from '../components/tooltip';

const IndexPage = () => {
  const { t, i18n, ready } = useTranslation(['searchStart', 'searchResults']);
  const { user } = useAuth();
  const router = useRouter();
  const { data: searchCriteria }: any = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateCountries = useUpdateCountries();
  const updateSearch = useUpdateSearch();

  /* need this lookup to be able to reset filtered countries
  (sets suggest list that appears when typing a jurisdiction)
  when returning to this page from a previous search
  */
  const geosQuery: any = useNestedLookups('geographies', '', 2);
  const {
    data: { data: { level1: regions = [], level2: countries = [] } = {} } = {},
  } = geosQuery;

  const exactMatchTooltip = t('Tooltips.Exact match', { ns: 'searchResults' });

  const handleSearchInput = (e, term) => {
    e.preventDefault();
    updateSearchCriteria.mutate({ ['query_string']: term });
    router.push('/search');
  };
  const handleSearchChange = (type: string, value: any) => {
    updateSearchCriteria.mutate({ [type]: value });
  };
  const handleLinkClick = (e) => {
    e.preventDefault();
    const term = e.currentTarget.textContent;
    handleSearchInput(e, term);
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
      regionName: '',
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
        <Layout
          title={`Climate Policy Radar | ${t('Law and Policy Search')}`}
          heading={t('Law and Policy Search')}
        >
          <div className="absolute inset-0 z-10 flex flex-col items-center justify-center">
            <AlphaLogo />
            <div className="container mt-24 md:mt-48 max-w-screen-lg mx-auto">
              <LandingSearchForm
                handleSearchInput={handleSearchInput}
                placeholder={t("Search for something, e.g. 'carbon taxes'")}
                input={searchCriteria.query_string}
              />
              <div className="mt-4 flex justify-end">
                <ExactMatch
                  landing={true}
                  checked={searchCriteria.exact_match}
                  id="exact-match"
                  handleSearchChange={handleSearchChange}
                />
                <div className="ml-2 -mt-1 text-sm">
                  <Tooltip id="exact_match" tooltip={exactMatchTooltip} />
                </div>
              </div>
              <div className="mt-12">
                <LandingPageLinks handleLinkClick={handleLinkClick} />
              </div>
            </div>
          </div>
        </Layout>
      )}
    </>
  );
};

export default IndexPage;
