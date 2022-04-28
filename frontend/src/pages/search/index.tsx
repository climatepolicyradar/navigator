import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
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
import TabbedNav from '../../components/nav/TabbedNav';
import Loader from '../../components/Loader';
import Sort from '../../components/filters/Sort';
import { CloseIcon, DownArrowIcon, DownloadIcon } from '../../components/Icons';
import Button from '../../components/buttons/Button';
import Close from '../../components/buttons/Close';


const Search = () => {
  const [showFilters, setShowFilters] = useState(false);
  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateSearchFilters = useUpdateSearchFilters();
  const { user } = useAuth();
  const router = useRouter();
  
  const { isFetching: isFetchingSearchCriteria, data: searchCriteria } = useSearchCriteria();
  const resultsQuery = useSearch('searches', searchCriteria);
  const { data: { documents } = [] } = resultsQuery;
  const { t, i18n, ready } = useTranslation('searchStart');
  const placeholder = t("Search for something, e.g. 'carbon taxes'");

  const documentCategories = ['All', 'Executive', 'Legislative', 'Litigation'];

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
  const handleSearchInput = (e, term) => {
    e.preventDefault();
    handleSearchChange('query_string', term);
  }
  const handleDocumentCategoryClick = (e) => {
    const val = e.currentTarget.textContent;
    const action = val === 'All' ? 'delete' : 'update';
    handleFilterChange('document_category', val, action);
  };
  const handleSortClick = (e) => {
    const val = e.currentTarget.value;
    const valArray = val.split(':');
    handleSearchChange('sort_field', valArray[0]);
    handleSearchChange('sort_order', valArray[1]);
  };
  const handleYearChange = (values) => {
    const newVals = values.map(value => value.toFixed(0))
    handleSearchChange('year_range', newVals);
  }
  const handleDocumentClick = () => {};

  useDidUpdateEffect(() => {
    resultsQuery.refetch();
  }, [searchCriteria]);

  useEffect(() => {

    if(router.query) {
      console.log(router.query.query_string)
      handleSearchChange('query_string', router.query.query_string as string);
    }
    
  }, [router])

  return (
    <>
    {/* {console.log(resultsQuery)} */}
      {isFetchingSearchCriteria || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Law and Policy Search')}`}
          heading={t('Law and Policy Search')}
        >
          <section>
            <div className="px-4 md:flex container">
              <div className="md:w-1/4 md:border-r border-blue-200 md:pr-8 flex-shrink-0">
                <div className="flex flex items-center justify-center w-full">
                  <button onClick={() => setShowFilters(!showFilters)} className="text-sm flex items-center bg-blue-500 mt-2 text-white flex-nowrap rounded-md px-4 py-2 md:hidden"><span>Filter</span> <div className="ml-2"><DownArrowIcon /></div></button>
                </div>
                
                <div className={`${showFilters ? '' : 'hidden'} relative md:block md:mt-8 mb-12 md:mb-0`}>
                  <div className="md:hidden absolute right-0 top-0">
                    <Close onClick={() => setShowFilters(false)} size="16" />
                  </div>
                  <SearchFilters
                    handleFilterChange={handleFilterChange}
                    searchCriteria={searchCriteria}
                    handleYearChange={handleYearChange}
                  />
                </div>
              </div>
              <div className="md:w-3/4">
                <div className="md:py-8 md:pl-8">
                  <p className="sm:hidden mt-4 mb-2">{placeholder}</p>
                  <SearchForm
                    placeholder={placeholder}
                    handleSearchInput={handleSearchInput}
                  />
                  <div className="flex justify-end mt-3">
                    <ExactMatch
                      checked={searchCriteria.exact_match}
                      id="exact-match"
                      handleSearchChange={handleSearchChange}
                    />
                  </div>
                </div>
                <div className="mt-4 relative">
                  <TabbedNav
                    items={documentCategories}
                    handleTabClick={handleDocumentCategoryClick}
                  />
                  <div className="mt-4 md:absolute right-0 top-0 md:-mt-2">
                    <Button
                      color="light-hover-dark"
                      extraClasses="text-sm py-1"
                    >
                      <div className="flex justify-center py-1">
                        <DownloadIcon />
                        <span>Download</span>
                      </div>
                    </Button>
                  </div>
                </div>
                <div className="mt-4 mb-8 flex justify-end">
                  <div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4 flex items-center">
                    <Sort updateSort={handleSortClick} />
                  </div>
                </div>

                <div className="md:pl-8 relative">
                  {resultsQuery.isLoading || !resultsQuery.isSuccess ? (
                    <div className="w-full flex justify-center h-96">
                      <Loader />
                    </div>
                  ) : (
                    documents.map((doc, index: number) => (
                      <div key={index} className="my-16 first:md:mt-4">
                        <SearchResult
                          document={doc}
                          onClick={handleDocumentClick}
                        />
                      </div>
                    ))
                  )}
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
