import { useEffect, useState, useRef } from "react";
import { useTranslation } from "react-i18next";
import { useAuth } from "@api/auth";
import { useDidUpdateEffect } from "@hooks/useDidUpdateEffect";
import useSearch from "@hooks/useSearch";
import useSearchCriteria from "@hooks/useSearchCriteria";
import useDocument from "@hooks/useDocument";
import useUpdateDocument from "@hooks/useUpdateDocument";
import useUpdateSearchCriteria from "@hooks/useUpdateSearchCriteria";
import useUpdateSearchFilters from "@hooks/useUpdateSearchFilters";
import useUpdateCountries from "@hooks/useUpdateCountries";
import useNestedLookups from "@hooks/useNestedLookups";
import useLookups from "@hooks/useLookups";
import useFilteredCountries from "@hooks/useFilteredCountries";
import useOutsideAlerter from "@hooks/useOutsideAlerter";
import useSortAndStructure from "@hooks/useSortAndStructure";
import Layout from "@components/layouts/Main";
import LoaderOverlay from "@components/LoaderOverlay";
import SearchForm from "@components/forms/SearchForm";
import SearchFilters from "@components/blocks/SearchFilters";
import TabbedNav from "@components/nav/TabbedNav";
import Loader from "@components/Loader";
import Sort from "@components/filters/Sort";
import Close from "@components/buttons/Close";
import FilterToggle from "@components/buttons/FilterToggle";
import Slideout from "@components/slideout";
import PassageMatches from "@components/PassageMatches";
import EmbeddedPDF from "@components/EmbeddedPDF";
import DocumentSlideout from "@components/headers/DocumentSlideout";
import Pagination from "@components/pagination";
import SearchResultList from "@components/blocks/SearchResultList";
import { initialSearchCriteria } from "@constants/searchCriteria";
import { PER_PAGE } from "@constants/paging";
import { calculatePageCount } from "@utils/paging";
import { TDocument } from "@types";

const Search = () => {
  const [showFilters, setShowFilters] = useState(false);
  const [showSlideout, setShowSlideout] = useState(false);
  const [showPDF, setShowPDF] = useState(false);
  const [passageIndex, setPassageIndex] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pageCount, setPageCount] = useState(1);
  const [offset, setOffset] = useState(0);
  const [noQuery, setNoQuery] = useState(true);
  const [categoryIndex, setCategoryIndex] = useState(0);

  const structureData = useSortAndStructure();
  const updateSearchCriteria = useUpdateSearchCriteria();
  const updateSearchFilters = useUpdateSearchFilters();
  const updateDocument = useUpdateDocument();
  const updateCountries = useUpdateCountries();
  const { user } = useAuth();
  const slideoutRef = useRef(null);

  // close slideout panel when clicking outside of it
  useOutsideAlerter(slideoutRef, (e) => {
    if (e.target.nodeName === "BUTTON") {
      return;
    }
    setShowSlideout(false);
  });

  // get lookups/filters
  const documentTypesQuery: any = useLookups("document_types");
  const { data: { data: documentTypes = {} } = {} } = documentTypesQuery;

  const geosQuery: any = useNestedLookups("geographies", "", 2);
  const { data: { data: { level1: regions = [], level2: countries = [] } = {} } = {} } = geosQuery;

  const { data: filteredCountries } = useFilteredCountries(countries);

  const sectorsQuery: any = useNestedLookups("sectors", "name");
  const { data: { data: { level1: sectors = [] } = {} } = {} } = sectorsQuery;

  const instrumentsQuery: any = useNestedLookups("instruments", "name");
  const { data: { data: { level1: instruments = [] } = {} } = {} } = instrumentsQuery;

  // search criteria and filters
  const { isFetching: isFetchingSearchCriteria, isSuccess: isSearchCriteriaSuccess, data: searchCriteria }: any = useSearchCriteria();

  // search results
  const resultsQuery: any = useSearch("searches", searchCriteria);
  const { data: { data: { documents = [] } = [] } = [], data: { data: { hits } = 0 } = 0, isSuccess } = resultsQuery;

  const { data: document }: { data: TDocument } = ({} = useDocument());
  const { t, ready } = useTranslation(["searchStart", "searchResults"]);
  const placeholder = t("Search for something, e.g. 'carbon taxes'");

  const documentCategories = ["All", "Executive", "Legislative", "Litigation"];

  const resetPaging = () => {
    setOffset(0);
    setPageNumber(1);
  };

  const resetSlideOut = (slideOut?: boolean) => {
    setShowPDF(false);
    setPassageIndex(null);
    setShowSlideout(slideOut ?? !showSlideout);
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
    setShowSlideout(false);
  };

  const handleFilterChange = (type: string, value: string, action: string = "update") => {
    resetPaging();
    updateSearchFilters.mutate({ [type]: value, action });
  };
  const handleSearchChange = (type: string, value: any) => {
    if (type !== "offset") resetPaging();
    updateSearchCriteria.mutate({ [type]: value });
  };
  const handleSearchInput = (e, term) => {
    e.preventDefault();
    handleSearchChange("query_string", term);
  };
  const handleDocumentCategoryClick = (e) => {
    const val = e.currentTarget.textContent;
    let category = val;
    // map to values that the api knows
    if (val === "Legislative") {
      category = "Law";
    }
    if (val === "Executive") {
      category = "Policy";
    }
    const action = val === "All" ? "delete" : "update";
    handleFilterChange("categories", category, action);
  };
  const handleSortClick = (e) => {
    const val = e.currentTarget.value;
    let field = null;
    let order = "desc";
    if (val !== "relevance") {
      const valArray = val.split(":");
      field = valArray[0];
      order = valArray[1];
    }
    handleSearchChange("sort_field", field);
    handleSearchChange("sort_order", order);
  };
  const handleYearChange = (values: number[]) => {
    const newVals = values.map((value: number) => Number(value).toFixed(0));
    handleSearchChange("year_range", newVals);
  };
  const handleClearSearch = () => {
    const { query_string, exact_match, sort_field, sort_order, ...initial } = initialSearchCriteria;
    updateSearchCriteria.mutate(initial);
    // reset filtered countries which show in suggest list
    // when typing in a jurisdiction/country
    updateCountries.mutate({
      regionName: "",
      regions,
      countries,
    });
  };
  const toggleFilters = () => {
    setShowFilters(!showFilters);
  };
  const handleDocumentClick = (e: any) => {
    // Check if we are clicking on the document matches button
    const id = e.target.dataset.docid;
    if (!id) return;

    // keep panel open if clicking a different document
    if (document?.document_id != id) {
      // setShowSlideout(true);
      resetSlideOut(true);
    } else {
      // setShowSlideout(!showSlideout);
      resetSlideOut();
    }
    updateDocument.mutate(id);

    // setShowPDF(false);
  };
  const getCurrentSortChoice = () => {
    const field = searchCriteria.sort_field;
    const order = searchCriteria.sort_order;
    if (field === null && order === "desc") {
      return "relevance";
    }
    return `${field}:${order}`;
  };
  const setCurrentCategoryIndex = () => {
    if (!searchCriteria?.keyword_filters?.categories) {
      setCategoryIndex(0);
      return;
    }
    let index = documentCategories.indexOf(searchCriteria.keyword_filters?.categories[0]);
    // ['All', 'Executive', 'Legislative', 'Litigation']
    // hack to get correct previously selected category
    if (searchCriteria.keyword_filters?.categories[0] === "Policy") {
      index = 1;
    }
    if (searchCriteria.keyword_filters?.categories[0] === "Law") {
      index = 2;
    }
    const catIndex = index === -1 ? 0 : index;
    setCategoryIndex(catIndex);
  };
  const getCurrentPage = () => {
    return searchCriteria?.offset / PER_PAGE + 1;
  };

  useDidUpdateEffect(() => {
    handleSearchChange("offset", offset);
    window.scrollTo(0, 0);
  }, [offset]);
  useEffect(() => {
    if (hits !== undefined) {
      setPageCount(calculatePageCount(hits));
    }
  }, [hits]);
  useDidUpdateEffect(() => {
    setOffset(searchCriteria?.offset);
    setCurrentCategoryIndex();
    if (searchCriteria?.query_string.length) {
      resultsQuery.refetch();
      setNoQuery(false);
    } else {
      setNoQuery(true);
    }
  }, [searchCriteria]);

  useEffect(() => {
    // get selected category if one previously selected
    setCurrentCategoryIndex();
    // get page number if returning from another page
    // gets page number based on the last offset set in the search criteria
    const currentPage = getCurrentPage();
    setPageNumber(currentPage);

    // check for search query on initial load
    if (searchCriteria?.query_string.length) {
      setNoQuery(false);
    }
    // fetch search results if they are empty and search query exists
    if (documents.length === 0 && searchCriteria?.query_string.length) {
      resultsQuery.refetch();
    }
  }, []);

  return (
    <>
      {isFetchingSearchCriteria || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Climate Policy Radar | ${t("Law and Policy Search")}`} heading={t("Law and Policy Search")}>
          <div onClick={handleDocumentClick}>
            <Slideout ref={slideoutRef} show={showSlideout} setShowSlideout={resetSlideOut}>
              <div className="flex flex-col h-full relative">
                <DocumentSlideout document={document} searchTerm={searchCriteria.query_string} showPDF={showPDF} setShowPDF={setShowPDF} />
                <div className="flex flex-col md:flex-row flex-1 h-0">
                  <div className={`${showPDF ? "hidden" : "block"} md:block md:w-1/3 overflow-y-scroll pl-3`}>
                    <PassageMatches document={document} setPassageIndex={setPassageIndex} setShowPDF={setShowPDF} activeIndex={passageIndex} />
                  </div>
                  <div className={`${showPDF ? "block" : "hidden"} md:block md:w-2/3 mt-4 px-6 flex-1`}>
                    <EmbeddedPDF document={document} passageIndex={passageIndex} />
                  </div>
                </div>
              </div>
            </Slideout>
            {showSlideout && <div className="w-full h-full bg-overlayWhite fixed top-0 z-30" />}
            <section>
              <div className="px-4 container">
                <div className="md:py-8 md:w-3/4 md:mx-auto">
                  <p className="sm:hidden mt-4 mb-2">{placeholder}</p>
                  <SearchForm placeholder={placeholder} handleSearchInput={handleSearchInput} input={searchCriteria.query_string} />
                </div>
              </div>
              <div className="px-4 md:flex container border-b border-blue-200">
                <div className="md:w-1/4 lg:w-[30%] xl:w-1/4 md:border-r border-blue-200 md:pr-8 flex-shrink-0">
                  <div className="flex md:hidden items-center justify-center w-full mt-4">
                    <FilterToggle toggle={toggleFilters} isOpen={showFilters} />
                  </div>

                  <div className={`${showFilters ? "" : "hidden"} relative md:block mb-12 md:mb-0`}>
                    <div className="md:hidden absolute right-0 top-0">
                      <Close onClick={() => setShowFilters(false)} size="16" />
                    </div>
                    {geosQuery.isFetching || sectorsQuery.isFetching || documentTypesQuery.isFetching || instrumentsQuery.isFetching ? (
                      <p>Loading filters...</p>
                    ) : (
                      <SearchFilters
                        handleFilterChange={handleFilterChange}
                        searchCriteria={searchCriteria}
                        handleYearChange={handleYearChange}
                        handleRegionChange={handleRegionChange}
                        handleClearSearch={handleClearSearch}
                        handleSearchChange={handleSearchChange}
                        regions={regions}
                        filteredCountries={filteredCountries}
                        sectors={sectors}
                        documentTypes={documentTypes}
                        instruments={structureData(instruments)}
                      />
                    )}
                  </div>
                </div>
                <div className="md:w-3/4">
                  <div className="mt-4 md:flex">
                    <div className="flex-grow">
                      <TabbedNav activeIndex={categoryIndex} items={documentCategories} handleTabClick={handleDocumentCategoryClick} />
                    </div>
                    <div className="mt-4 md:-mt-2 md:ml-2 lg:ml-8 md:mb-2 flex items-center">
                      <Sort defaultValue={getCurrentSortChoice()} updateSort={handleSortClick} />
                    </div>
                    {/* Hide download button until this functionality is implemented in back end */}
                    {/* <div className="mt-4 md:absolute right-0 top-0 md:-mt-2 flex z-10">
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
                        <Tooltip
                          id="download-tt"
                          tooltip={downloadCSVTooltip}
                        />
                      </div>
                    </div> */}
                  </div>

                  <div className="search-results md:pl-8 md:mt-12 relative">
                    {resultsQuery.isFetching ? (
                      <div className="w-full flex justify-center h-96">
                        <Loader />
                      </div>
                    ) : noQuery ? (
                      <p className="mt-4 font-bold text-red-500 h-96">
                        {/* TODO: make text translatable */}
                        Please enter some search terms.
                      </p>
                    ) : (
                      <SearchResultList searchCriteria={searchCriteria} documents={documents} />
                    )}
                  </div>
                </div>
              </div>
            </section>
            {pageCount > 1 && !noQuery && (
              <section>
                <div className="mb-12">
                  <Pagination pageNumber={pageNumber} pageCount={pageCount} onChange={handlePageChange} />
                </div>
              </section>
            )}
          </div>
        </Layout>
      )}
    </>
  );
};
export default Search;
