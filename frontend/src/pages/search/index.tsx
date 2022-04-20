import { useEffect } from 'react';
import Layout from '../../components/layouts/Main';
import LoaderOverlay from '../../components/LoaderOverlay';
import useSearch from '../../hooks/useSearch';
import useLookups from '../../hooks/useLookups';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../api/auth';
import { getCountryFromId } from '../../utils/geography';
import SearchForm from '../../components/forms/SearchForm';
import SearchResult from '../../components/text-blocks/SearchResult';

const Search = () => {
  const { user } = useAuth();
  const resultsQuery = useSearch('searches');
  const { data: { documents } = [] } = resultsQuery;
  const geosQuery = useLookups('geographies');
  const { data: geographies } = geosQuery;
  const { t, i18n, ready } = useTranslation(['searchResults', 'searchStart']);
  const placeholder = t("Search for something, e.g. 'carbon taxes'", {
    ns: 'searchStart',
  });
  const handleDocumentClick = () => {};

  useEffect(() => {
    // console.log(resultsQuery);
  }, [resultsQuery]);
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
            <div className="px-4 md:flex md:border-b">
              <div className="md:w-1/3 lg:w-1/4 md:border-r border-indigo-200">
                <div className="text-indigo-400 mt-8 font-medium">
                  {t('Filter by')}
                </div>
              </div>
              <div className="md:w-2/3 lg:w-3/4 xl:w-3/5">
                <div className="md:py-8 md:pl-8">
                  <p className="sm:hidden mt-4">{placeholder}</p>
                  <SearchForm placeholder={placeholder} />
                </div>
                <div className="md:pl-8">
                  {documents.map((doc, index: number) => (
                    <div key={index} className="my-4">
                      <SearchResult
                        document={doc}
                        onClick={handleDocumentClick}
                      />
                      {/* <p className="font-bold">{doc.document_name}</p>
                      <p>
                        {getCountryFromId(doc.document_country_code, geographies)}
                      </p>
                      <p>{doc.document_description}</p> */}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};
export default Search;
