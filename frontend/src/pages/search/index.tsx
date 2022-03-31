import Layout from '../../components/layouts/Main';
import LoaderOverlay from '../../components/LoaderOverlay';
import useActions from '../../hooks/useActions';
import useLookups from '../../hooks/useLookups';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../api/auth';
import { getCountryFromId } from '../../utils/geography';

const Search = () => {
  const { user } = useAuth();
  const resultsQuery = useActions('actions');
  const { data: results } = resultsQuery;
  const geosQuery = useLookups('geographies');
  const { data: geographies } = geosQuery;
  const { t, i18n, ready } = useTranslation('searchResults');

  return (
    <>
      {!resultsQuery.isSuccess || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Law and policy search')}`}
          heading={t('Law and policy search')}
        >
          <section>
            <div className="container py-4">
              {results.items.map((result, index: number) => (
                <div key={index} className="my-4">
                  <p className="font-bold">{result.name}</p>
                  <p>{getCountryFromId(result.geography_id, geographies)}</p>
                  <p>{result.description}</p>
                </div>
              ))}
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};
export default Search;
