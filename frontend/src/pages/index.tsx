import Layout from '../components/layouts/FullPageBanner';
import Dashboard from '../components/Dashboard';
import SearchForm from '../components/forms/SearchForm';
// import i18n (needs to be bundled ;))
import './i18n';
import { useTranslation } from 'react-i18next';

const IndexPage = () => {
  const { t, i18n } = useTranslation('search-start');
  return (
    <>
      {!i18n.store.data.hasOwnProperty('en') ? (
        <div>Loading...</div>
      ) : (
        <Layout title={`Navigator | ${t('title')}`} heading={t('title')}>
          <div className="absolute top-0 left-0 w-full z-10 mt-52 md:mt-44 ">
            <div className="container py-4 overflow-x-hidden">
              <Dashboard
                terms={[
                  t('dashboard.panel1'),
                  t('dashboard.panel2'),
                  t('dashboard.panel3'),
                ]}
              />
              <SearchForm
                placeholder={t('searchPlaceholder')}
                buttonText={t('searchButtonText')}
              />
            </div>
          </div>
        </Layout>
      )}
    </>
  );
};

export default IndexPage;
