import { convertDate } from "@utils/timedate";
import { DocumentListItem } from "@components/document/DocumentListItem";
import { TDocument } from "@types";

interface SearchResultProps {
  document: TDocument;
}

const SearchResult = ({ document }: SearchResultProps) => {
  const {
    document_geography,
    document_country_english_shortname,
    document_slug,
    document_date,
    document_description,
    document_name,
    document_category,
    document_title_match,
    document_description_match,
    document_passage_matches,
    document_content_type,
  } = document;

  const formatDate = () => {
    const eudate = document_date;
    const dateArr = eudate.split("/");
    return `${dateArr[1]}/${dateArr[0]}/${dateArr[2]}`;
  };
  const [year] = convertDate(formatDate());

  const showMatches = () => {
    if (document_passage_matches.length || document_title_match || document_description_match) {
      return (
        <>
          <div className="w-full lg:w-auto flex flex-nowrap mt-2 lg:mt-0 lg:mr-4">
            {/* TODO: translate below text, how to handle plurals? */}
            <span className="font-medium lg:ml-10 mr-2">Matches:</span>
            <div className="divide-x divide-current flex-grow-0">
              {document_title_match && <span className="px-2">Title</span>}
              {document_description_match && <span className="px-2">Summary</span>}
              {document_passage_matches.length > 0 && <span className="px-2">Document</span>}
            </div>
          </div>
          {document_content_type === "application/pdf" && document_passage_matches.length > 0 && (
            <button data-slug={document_slug} className="mt-2 lg:mt-0 py-1 px-4 bg-blue-600 text-white font-medium transition duration-300 rounded-lg hover:bg-indigo-600">
              {`See ${document_passage_matches.length} match${document_passage_matches.length > 1 ? "es" : ""} in document`}
            </button>
          )}
        </>
      );
    }
  };

  return (
    <DocumentListItem
      listItem={{
        slug: document_slug,
        name: document_name,
        country_code: document_geography,
        country_name: document_country_english_shortname,
        document_year: year,
        description: document_description,
        category: document_category,
      }}
    >
      {showMatches()}
    </DocumentListItem>
  );
};
export default SearchResult;
