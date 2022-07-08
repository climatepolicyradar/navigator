import { truncateString } from '../../helpers';
import Link from 'next/link';
import { convertDate } from '../../utils/timedate';

interface SearchResultProps {
  document: any;
}

const SearchResult = ({ document }: SearchResultProps) => {
  const formatDate = () => {
    const eudate = document.document_date;
    const dateArr = eudate.split('/');
    return `${dateArr[1]}/${dateArr[0]}/${dateArr[2]}`;
  };
  const [year, day, month] = convertDate(formatDate());

  const showMatches = () => {
    if (
      document.document_passage_matches.length ||
      document.document_title_match ||
      document.document_description_match
    ) {
      return (
        <>
          <div className="w-full lg:w-auto flex flex-nowrap mt-2 lg:mt-0 ">
            {/* TODO: translate below text, how to handle plurals? */}
            <span className="font-medium lg:ml-10 mr-2">Matches</span>
            <div className="divide-x divide-current flex-grow-0">
              {document.document_title_match && (
                <span className="px-2">Title</span>
              )}
              {document.document_description_match && (
                <span className="px-2">Summary</span>
              )}
              {document.document_passage_matches.length > 0 && (
                <span className="px-2">Document</span>
              )}
            </div>
          </div>
          {document.document_content_type === 'application/pdf' &&
            document.document_passage_matches.length > 0 && (
              <button
                data-docid={document.document_id}
                className="lg:ml-4 mt-2 lg:mt-0 py-1 px-4 bg-blue-600 text-white font-medium transition duration-300 hover:bg-indigo-600"
              >
                See {document.document_passage_matches.length} match
                {document.document_passage_matches.length > 1 ? 'es' : ''}
              </button>
            )}
        </>
      );
    }
  };

  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-center">
          <Link href={`/document/${document.document_id}`}>
            <a className="text-left font-medium text-lg leading-tight">
              {truncateString(document.document_name, 80)}
            </a>
          </Link>
        </h2>
      </div>

      <div className="flex flex-wrap lg:flex-nowrap text-sm text-indigo-400 mt-4 items-center">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`}
        />
        <span className="ml-2">
          {document.document_country_english_shortname}
        </span>
        <span className="ml-4">{year}</span>
        {showMatches()}
      </div>

      <p className="text-indigo-400 mt-3">
        {truncateString(
          document.document_description.replace(/(<([^>]+)>)/gi, ''),
          375
        )}
      </p>
    </div>
  );
};
export default SearchResult;
