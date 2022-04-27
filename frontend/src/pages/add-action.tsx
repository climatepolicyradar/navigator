import Layout from '../components/layouts/Main';
import AddAction from '../components/forms/AddAction';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';

import useLookups from '../hooks/useLookups';
import { useAuth } from '../api/auth';

const AddActionPage = () => {
  const geosQuery = useLookups('geographies');
  const langsQuery = useLookups('languages');
  const sourcesQuery = useLookups('sources');

  const { user } = useAuth();

  const { t, i18n, ready } = useTranslation('addAction');

  return (
    <>
      {!ready ||
      !user ||
      !geosQuery.isSuccess ||
      !langsQuery.isSuccess ||
      !sourcesQuery.isSuccess ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Add Action')}`}
          heading={t('Add Action')}
        >
          <section>
            <div className="container py-4">
              <AddAction
                geographies={geosQuery?.data}
                languages={langsQuery?.data}
                actionTypes={[]}
                sources={sourcesQuery?.data}
              />
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};

export default AddActionPage;
