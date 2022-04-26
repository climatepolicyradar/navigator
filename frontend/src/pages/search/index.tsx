import { useEffect, useState } from 'react';
import { useDidUpdateEffect } from '../../hooks/useDidUpdateEffect';
import Layout from '../../components/layouts/Main';
import LoaderOverlay from '../../components/LoaderOverlay';
import useSearch from '../../hooks/useSearch';
import useSearchCriteria from '../../hooks/useSearchCriteria';
import useUpdateSearchCriteria from '../../hooks/useUpdateSearchCriteria';
import useUpdateSearchFilters from '../../hooks/useUpdateSearchFilters';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../api/auth';
import SearchForm from '../../components/forms/SearchForm';
import SearchResult from '../../components/text-blocks/SearchResult';
import SearchFilters from '../../components/SearchFilters';
import ExactMatch from '../../components/filters/ExactMatch';
import DocumentCategories from '../../components/nav/DocumentCategories';

const Search = () => {
  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateSearchFilters = useUpdateSearchFilters();
  const { data: searchCriteria } = useSearchCriteria();

  const { user } = useAuth();
  const resultsQuery = useSearch('searches', searchCriteria);
  const { data: { documents } = [] } = resultsQuery;
  const { t, i18n, ready } = useTranslation('searchStart');
  const placeholder = t("Search for something, e.g. 'carbon taxes'");

  const handleFilterChange = (
    type: string,
    value: string,
    action: string = 'update'
  ) => {
    updateSearchFilters.mutate({ [type]: value, action });
  };
  const handleSearchChange = (type: string, value: string) => {
    updateSearchCriteria.mutate({ [type]: value });
  };

  const handleDocumentClick = () => {};

  useDidUpdateEffect(() => {
    resultsQuery.refetch();
  }, [searchCriteria]);

  return (
    <>
      {!resultsQuery.isSuccess || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Law and Policy Search')}`}
          heading={t('Law and Policy Search')}
        >
          <section>
            <div className="px-4 md:flex container">
              <div className="md:w-1/4 lg:w-1/4 md:border-r border-blue-200 pr-8 flex-shrink-0">
                <SearchFilters
                  handleFilterChange={handleFilterChange}
                  searchCriteria={searchCriteria}
                />
              </div>
              <div>
                <div className="md:py-8 md:pl-8">
                  <p className="sm:hidden mt-4">{placeholder}</p>
                  <SearchForm
                    placeholder={placeholder}
                    handleSearchChange={handleSearchChange}
                  />
                  <div className="flex justify-end mt-3">
                    <ExactMatch
                      checked={searchCriteria.exact_match}
                      id="exact-match"
                      handleSearchChange={handleSearchChange}
                    />
                  </div>
                </div>
                <div className="mt-4">
                  <DocumentCategories handleFilterChange={handleFilterChange} />
                </div>
                {/* TODO: sort by */}
                <div className="mt-4 flex justify-end">Sort by</div>
                <div className="md:pl-8">
                  {documents.map((doc, index: number) => (
                    <div key={index} className="my-16 first:mt-4">
                      <SearchResult
                        document={doc}
                        onClick={handleDocumentClick}
                      />
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
