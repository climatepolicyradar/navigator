import { truncateString } from '../../helpers';
import Link from 'next/link';
import { convertDate } from '../../utils/timedate';

interface SearchResultProps {
  document: any;
  onClick(): void;
}

const SearchResult = ({ document, onClick }: SearchResultProps) => {
  const formatDate = () => {
    const eudate = document.document_date;
    const dateArr = eudate.split('/');
    return `${dateArr[1]}/${dateArr[0]}/${dateArr[2]}`;
  };
  const [year, day, month] = convertDate(formatDate());

  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-center">
          <Link href={`/document/${document.document_id}`}>
            <a className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight">
              {truncateString(document.document_name, 80)}
              <br />
              <span className="text-xs text-indigo-500 font-normal">
                (Click to see document overview)
              </span>
            </a>
          </Link>
        </h2>
      </div>

      <div className="flex text-sm text-indigo-400 mt-4">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`}
        />
        <span className="ml-2">
          {document.document_country_english_shortname}
        </span>
        <span className="ml-6">{`${day} ${month} ${year}`}</span>
      </div>
      {/* TODO: translate below text, how to handle plurals? */}
      {document.document_passage_matches.length > 0 &&
        document.document_content_type === 'application/pdf' && (
          <div className="my-2 font-medium">
            <span className="text-indigo-500">Click here to see &nbsp;</span>
            <button
              className="font-medium text-base text-indigo-600 underline text-sm mt-3 transition duration-300 hover:text-blue-500"
              onClick={onClick}
            >
              {document.document_passage_matches.length} match
              {`${
                document.document_passage_matches.length === 1 ? '' : 'es'
              }`}{' '}
              in document
            </button>
          </div>
        )}
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
