import SearchResult from './SearchResult';

const SearchResultList = ({ searchCriteria, documents }) => {
  if (
    searchCriteria?.keyword_filters?.categories &&
    searchCriteria?.keyword_filters?.categories[0] === 'Litigation'
  ) {
    return (
      // TODO: translate
      <div className="h-96">
        Climate litigation case documents are coming soon to Climate Policy
        Radar! In the meantime, head to{' '}
        <a
          className="text-blue-500 transition duration-300 hover:text-indigo-600"
          href="https://climate-laws.org/litigation_cases"
        >
          climate-laws.org/litigation_cases
        </a>
      </div>
    );
  }
  if (
    searchCriteria.keyword_filters?.categories &&
    searchCriteria.keyword_filters?.categories[0] === 'Legislative' &&
    documents.length === 0
  ) {
    return (
      <div className="h-96">
        Your search returned no results from documents in the legislative
        category. Please try the executive category, or conduct a new search.
      </div>
    );
  }
  if (
    searchCriteria.keyword_filters?.categories &&
    searchCriteria.keyword_filters?.categories[0] === 'Executive' &&
    documents.length === 0
  ) {
    return (
      <div className="h-96">
        Your search returned no results from documents in the executive
        category. Please try the legislative category, or conduct a new search.
      </div>
    );
  }
  if (documents.length === 0) {
    return <div className="h-96">Your search returned no results.</div>;
  }
  return documents?.map((doc: any, index: number) => (
    <div key={index} className="my-16 first:md:mt-4">
      <SearchResult document={doc} />
    </div>
  ));
};
export default SearchResultList;
