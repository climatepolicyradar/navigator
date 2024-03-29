import { ExternalLink } from "@components/ExternalLink";
import SearchResult from "./SearchResult";

const SearchResultList = ({ searchCriteria, documents }) => {
  if (searchCriteria?.keyword_filters?.categories && searchCriteria?.keyword_filters?.categories[0] === "Litigation") {
    return (
      // TODO: translate
      <div className="h-96 mt-4 md:mt-0">
        Climate litigation case documents are coming soon. In the meantime, visit the Sabin Center’s{" "}
        <ExternalLink url="http://climatecasechart.com/">Climate Change Litigation Databases</ExternalLink>.
      </div>
    );
  }
  if (searchCriteria.keyword_filters?.categories && searchCriteria.keyword_filters?.categories[0] === "Legislative" && documents.length === 0) {
    return (
      <div className="h-96 mt-4 md:mt-0">
        Your search returned no results from documents in the legislative category. Please try the executive category, or conduct a new search.
      </div>
    );
  }
  if (searchCriteria.keyword_filters?.categories && searchCriteria.keyword_filters?.categories[0] === "Executive" && documents.length === 0) {
    return (
      <div className="h-96 mt-4 md:mt-0">
        Your search returned no results from documents in the executive category. Please try the legislative category, or conduct a new search.
      </div>
    );
  }
  if (documents.length === 0) {
    return <div className="h-96 mt-4 md:mt-0">Your search returned no results.</div>;
  }
  return documents?.map((doc: any, index: number) => (
    <div key={index} className="my-16 first:md:mt-4">
      <SearchResult document={doc} />
    </div>
  ));
};
export default SearchResultList;
