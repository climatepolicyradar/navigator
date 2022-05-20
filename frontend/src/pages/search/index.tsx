import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useDidUpdateEffect } from '../../hooks/useDidUpdateEffect';
import Layout from '../../components/layouts/Main';
import LoaderOverlay from '../../components/LoaderOverlay';
import useSearch from '../../hooks/useSearch';
import useSearchCriteria from '../../hooks/useSearchCriteria';
import useDocument from '../../hooks/useDocument';
import useUpdateDocument from '../../hooks/useUpdateDocument';
import useUpdateSearchCriteria from '../../hooks/useUpdateSearchCriteria';
import useUpdateSearchFilters from '../../hooks/useUpdateSearchFilters';
import useUpdateCountries from '../../hooks/useUpdateCountries';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../../api/auth';
import SearchForm from '../../components/forms/SearchForm';
import SearchResult from '../../components/blocks/SearchResult';
import SearchFilters from '../../components/SearchFilters';
import ExactMatch from '../../components/filters/ExactMatch';
import TabbedNav from '../../components/nav/TabbedNav';
import Loader from '../../components/Loader';
import Sort from '../../components/filters/Sort';
import { DownloadIcon } from '../../components/svg/Icons';
import Button from '../../components/buttons/Button';
import Close from '../../components/buttons/Close';
import FilterToggle from '../../components/buttons/FilterToggle';
import Slideout from '../../components/slideout';
import PassageMatches from '../../components/PassageMatches';
import EmbeddedPDF from '../../components/EmbeddedPDF';
import DocumentSlideout from '../../components/headers/DocumentSlideout';
import Tooltip from '../../components/tooltip';
import { calculatePageCount } from '../../utils/paging';
import Pagination from '../../components/pagination';
import { PER_PAGE } from '../../constants/paging';
import useNestedLookups from '../../hooks/useNestedLookups';
import useLookups from '../../hooks/useLookups';
import useFilteredCountries from '../../hooks/useFilteredCountries';
import SearchResultList from '../../components/blocks/SearchResultList';

const Search = () => {
  const [showFilters, setShowFilters] = useState(false);
  const [showSlideout, setShowSlideout] = useState(false);
  const [showPDF, setShowPDF] = useState(false);
  const [passageIndex, setPassageIndex] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageCount, setPageCount] = useState(1);
  const [offset, setOffset] = useState(0);
  const [noQuery, setNoQuery] = useState(false);

  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateSearchFilters = useUpdateSearchFilters();
  const updateDocument = useUpdateDocument();
  const updateCountries = useUpdateCountries();
  const { user } = useAuth();
  const router = useRouter();

  // lookups/filters
  const {
    nestedLookupsQuery: geosQuery,
    level1: regions,
    level2: countries,
  } = useNestedLookups('geographies', '', 2);
  const { data: filteredCountries } = useFilteredCountries(countries);
  const { nestedLookupsQuery: sectorsQuery, level1: sectors } =
    useNestedLookups('sectors', 'name');
  const { lookupsQuery: documentTypesQuery, list: documentTypes } =
    useLookups('document_types');
  const { nestedLookupsQuery: instrumentsQuery, level1: instruments } =
    useNestedLookups('instruments', 'name');

  const {
    isFetching: isFetchingSearchCriteria,
    isSuccess: isSearchCriteriaSuccess,
    data: searchCriteria,
  }: any = useSearchCriteria();
  const resultsQuery: any = useSearch('searches', searchCriteria);

  const {
    data: { data: { documents } = [] } = [],
    data: { data: { hits } = 0 } = 0,
    isSuccess,
  } = resultsQuery;
  const document: any = useDocument();
  const { t, i18n, ready } = useTranslation(['searchStart', 'searchResults']);
  const placeholder = t("Search for something, e.g. 'carbon taxes'");

  const documentCategories = ['All', 'Executive', 'Legislative', 'Litigation'];

  const resetPaging = () => {
    setOffset(0);
    setPageNumber(1);
  };

  const handleRegionChange = (type, regionName) => {
    handleFilterChange(type, regionName);
    updateCountries.mutate({
      regionName,
      regions,
      countries,
    });
  };
  const handlePageChange = (page: number) => {
    setPageNumber(page);
    setOffset((page - 1) * PER_PAGE);
  };

  const handleFilterChange = (
    type: string,
    value: string,
    action: string = 'update'
  ) => {
    resetPaging();
    updateSearchFilters.mutate({ [type]: value, action });
  };
  const handleSearchChange = (type: string, value: any) => {
    if (type !== 'offset') resetPaging();
    updateSearchCriteria.mutate({ [type]: value });
  };
  const handleSearchInput = (e, term) => {
    e.preventDefault();
    handleSearchChange('query_string', term);
  };
  const handleDocumentCategoryClick = (e) => {
    const val = e.currentTarget.textContent;
    let category = val;
    // map to values that the api knows
    if (val === 'Legislative') {
      category = 'Law';
    }
    if (val === 'Executive') {
      category = 'Policy';
    }
    const action = val === 'All' ? 'delete' : 'update';
    handleFilterChange('categories', category, action);
  };
  const handleSortClick = (e) => {
    const val = e.currentTarget.value;
    let field = null;
    let order = 'desc';
    if (val !== 'relevance') {
      const valArray = val.split(':');
      field = valArray[0];
      order = valArray[1];
    }
    handleSearchChange('sort_field', field);
    handleSearchChange('sort_order', order);
  };
  const handleYearChange = (values) => {
    const newVals = values.map((value) => value.toFixed(0));
    handleSearchChange('year_range', newVals);
  };
  const toggleFilters = () => {
    setShowFilters(!showFilters);
  };
  const handleDocumentClick = (id) => {
    updateDocument.mutate(id);
    const doc = documents.find((item) => item.document_id === id);
    if (doc.document_passage_matches.length > 0) {
      setShowSlideout(true);
      setShowPDF(false);
    } else {
      router.push(`/document/${id}`);
    }
  };
  const getCurrentSortChoice = () => {
    const field = searchCriteria.sort_field;
    const order = searchCriteria.sort_order;
    if (field === null && order === 'desc') {
      return 'relevance';
    }
    return `${field}:${order}`;
  };
  const getCurrentCategoryIndex = () => {
    if (!searchCriteria.keyword_filters?.categories) return 0;
    let index = documentCategories.indexOf(
      searchCriteria.keyword_filters?.categories[0]
    );
    // ['All', 'Executive', 'Legislative', 'Litigation']
    // hack to get correct previously selected category
    if (searchCriteria.keyword_filters?.categories[0] === 'Policy') {
      index = 1;
    }
    if (searchCriteria.keyword_filters?.categories[0] === 'Law') {
      index = 2;
    }
    return index === -1 ? 0 : index;
  };

  useDidUpdateEffect(() => {
    handleSearchChange('offset', offset);
    window.scrollTo(0, 0);
  }, [offset]);
  useEffect(() => {
    if (hits) {
      setPageCount(calculatePageCount(hits));
    }
  }, [hits]);
  useEffect(() => {
    if (searchCriteria?.query_string.length) {
      resultsQuery.refetch();
      setNoQuery(false);
    } else {
      setNoQuery(true);
    }
  }, [searchCriteria]);

  const exactMatchTooltip = t('Tooltips.Exact match', { ns: 'searchResults' });
  const sortByTooltip = t('Tooltips.Sort by', { ns: 'searchResults' });
  const downloadCSVTooltip = t('Tooltips.Download CSV', {
    ns: 'searchResults',
  });

  return (
    <>
      {isFetchingSearchCriteria || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Climate Policy Radar | ${t('Law and Policy Search')}`}
          heading={t('Law and Policy Search')}
        >
          <Slideout show={showSlideout} setShowSlideout={setShowSlideout}>
            <div className="flex flex-col h-full">
              <DocumentSlideout
                document={document.data}
                setShowPDF={setShowPDF}
                showPDF={showPDF}
                setPassageIndex={setPassageIndex}
              />
              {showPDF ? (
                <div className="mt-4 px-6 flex-1">
                  <EmbeddedPDF
                    document={document.data}
                    passageIndex={passageIndex}
                    setShowPDF={setShowPDF}
                  />
                </div>
              ) : (
                <PassageMatches
                  document={document}
                  setPassageIndex={setPassageIndex}
                  setShowPDF={setShowPDF}
                />
              )}
            </div>
          </Slideout>
          <section>
            <div className="px-4 md:flex container border-b border-blue-200">
              <div className="md:w-1/4 md:border-r border-blue-200 md:pr-8 flex-shrink-0">
                <div className="flex flex items-center justify-center w-full">
                  <FilterToggle toggle={toggleFilters} />
                </div>

                <div
                  className={`${
                    showFilters ? '' : 'hidden'
                  } relative md:block md:mt-8 mb-12 md:mb-0`}
                >
                  <div className="md:hidden absolute right-0 top-0">
                    <Close onClick={() => setShowFilters(false)} size="16" />
                  </div>
                  {geosQuery.isFetching ||
                  sectorsQuery.isFetching ||
                  documentTypesQuery.isFetching ||
                  instrumentsQuery.isFetching ? (
                    <p>Loading filters...</p>
                  ) : (
                    <SearchFilters
                      handleFilterChange={handleFilterChange}
                      searchCriteria={searchCriteria}
                      handleYearChange={handleYearChange}
                      handleRegionChange={handleRegionChange}
                      regions={regions}
                      filteredCountries={filteredCountries}
                      sectors={sectors}
                      documentTypes={documentTypes}
                      instruments={instruments}
                    />
                  )}
                </div>
              </div>
              <div className="md:w-3/4">
                <div className="md:py-8 md:pl-8">
                  <p className="sm:hidden mt-4 mb-2">{placeholder}</p>
                  <SearchForm
                    placeholder={placeholder}
                    handleSearchInput={handleSearchInput}
                    input={searchCriteria.query_string}
                  />
                  <div className="flex justify-end mt-3">
                    <ExactMatch
                      checked={searchCriteria.exact_match}
                      id="exact-match"
                      handleSearchChange={handleSearchChange}
                    />
                    <div className="ml-1 -mt-1 text-sm">
                      <Tooltip id="exact_match" tooltip={exactMatchTooltip} />
                    </div>
                  </div>
                </div>
                <div className="mt-4 relative z-10">
                  <TabbedNav
                    activeIndex={getCurrentCategoryIndex()}
                    items={documentCategories}
                    handleTabClick={handleDocumentCategoryClick}
                  />
                  <div className="mt-4 md:absolute right-0 top-0 md:-mt-2 flex z-10">
                    <Button
                      color="light-hover-dark"
                      thin={true}
                      disabled={true}
                      extraClasses="text-sm"
                    >
                      <div className="flex justify-center py-1">
                        <DownloadIcon />
                        <span>Download</span>
                      </div>
                    </Button>
                    <div className="ml-1 mt-1">
                      <Tooltip id="download-tt" tooltip={downloadCSVTooltip} />
                    </div>
                  </div>
                </div>
                <div className="mt-4 mb-8 flex justify-end">
                  <div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4 flex items-center">
                    <Sort
                      defaultValue={getCurrentSortChoice()}
                      updateSort={handleSortClick}
                    />
                    <div className="ml-1 -mt-1">
                      <Tooltip id="sortby-tt" tooltip={sortByTooltip} />
                    </div>
                  </div>
                </div>

                <div className="md:pl-8 relative">
                  {resultsQuery.isFetching || !resultsQuery.isSuccess ? (
                    <div className="w-full flex justify-center h-96">
                      <Loader />
                    </div>
                  ) : noQuery ? (
                    <p className="font-bold text-red-500">
                      Please enter some search terms.
                    </p>
                  ) : (
                    <SearchResultList
                      searchCriteria={searchCriteria}
                      documents={documents}
                      handleDocumentClick={handleDocumentClick}
                    />
                  )}
                </div>
              </div>
            </div>
          </section>
          {pageCount > 1 && !noQuery && (
            <section>
              <div className="mb-12">
                <Pagination
                  pageNumber={pageNumber}
                  pageCount={pageCount}
                  onChange={handlePageChange}
                />
              </div>
            </section>
          )}
        </Layout>
      )}
    </>
  );
};
export default Search;
