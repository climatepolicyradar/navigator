import { useRouter } from 'next/router';
import Layout from '../components/layouts/LandingPage';
import Dashboard from '../components/dashboard';
import SearchForm from '../components/forms/SearchForm';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import { useAuth } from '../api/auth';
import useSearchCriteria from '../hooks/useSearchCriteria';
import useUpdateSearchCriteria from '../hooks/useUpdateSearchCriteria';
import LandingSearchForm from '../components/forms/LandingSearchForm';
import AlphaLogo from '../components/logo';
import ExactMatch from '../components/filters/ExactMatch';
import Summary from '../components/blocks/Summary';
import LandingPageLinks from '../components/blocks/LandingPageLinks';

const IndexPage = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const { user } = useAuth();
  const router = useRouter();
  const { data: searchCriteria }: any = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
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

  return (
    <>
      {!ready || !user || !searchCriteria ? (
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
