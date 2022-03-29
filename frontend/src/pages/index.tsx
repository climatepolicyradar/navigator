import Layout from '../components/layouts/FullPageBanner';
import Dashboard from '../components/Dashboard';
import SearchForm from '../components/forms/SearchForm';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import { useAuth } from '../api/auth';

const IndexPage = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const { user } = useAuth();

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
              <SearchForm
                placeholder={t("Search for something, e.g. 'carbon taxes'")}
                buttonText={t('Go')}
              />
            </div>
          </div>
        </Layout>
      )}
    </>
  );
};

export default IndexPage;
