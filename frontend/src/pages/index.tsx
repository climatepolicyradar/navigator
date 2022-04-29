import { useRouter } from 'next/router';
import Layout from '../components/layouts/FullPageBanner';
import Dashboard from '../components/Dashboard';
import SearchForm from '../components/forms/SearchForm';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import { useAuth } from '../api/auth';
import useSearchCriteria from '../hooks/useSearchCriteria';
import useUpdateSearchCriteria from '../hooks/useUpdateSearchCriteria';

const IndexPage = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const { user } = useAuth();
  const router = useRouter();
  const searchCriteria = useSearchCriteria();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const handleSearchInput = (e, term) => {
    e.preventDefault();
    updateSearchCriteria.mutate({ ['query_string']: term });
    router.push('/search');
  };

  return (
    <>
      {!ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Law and Policy Search')}`}
          heading={t('Law and Policy Search')}
        >
          <div className="absolute top-0 left-0 w-full z-10 mt-52 md:mt-44 ">
            <div className="container py-4 overflow-x-hidden">
              <Dashboard
                terms={[
                  t('dashboard.Documents'),
                  t('dashboard.Jurisdictions'),
                  t('dashboard.New Documents'),
                ]}
              />
              <div className="mt-8 md:mt-16">
                <p className="sm:hidden mt-4 text-center text-white mb-4">
                  {t("Search for something, e.g. 'carbon taxes'")}
                </p>

                <SearchForm
                  handleSearchInput={handleSearchInput}
                  placeholder={t("Search for something, e.g. 'carbon taxes'")}
                />
              </div>
            </div>
          </div>
        </Layout>
      )}
    </>
  );
};

export default IndexPage;
