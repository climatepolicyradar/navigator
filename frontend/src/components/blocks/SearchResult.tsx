import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { DownloadPDFIcon, ViewDocumentCoverPageIcon } from '../svg/Icons';
import { truncateString } from '../../helpers';
import Tooltip from '../tooltip';

interface SearchResultProps {
  document: any;
  onClick(): void;
}

const SearchResult = ({ document, onClick }: SearchResultProps) => {
  const router = useRouter();

  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <button
            onClick={onClick}
            className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight"
          >
            {truncateString(document.document_name, 80)}
          </button>
        </h2>

        <div className="flex pl-2">
          <a target="_blank" href={document.document_url}>
            <span className="sr-only">Download PDF</span>
            <DownloadPDFIcon height="24" width="24" />
          </a>
          <button
            className="text-indigo-500 hover:text-indigo-600 transition duration-300 ml-2"
            onClick={() => router.push(`/document/${document.document_id}`)}
          >
            <ViewDocumentCoverPageIcon height="24" width="24" />
          </button>
        </div>
      </div>

      <div className="flex text-xs text-indigo-400 mt-3">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`}
        />
        <span className="ml-2">
          {document.document_country_english_shortname}
        </span>
        <span className="ml-6">{document.document_date}</span>
        <div className="ml-1 -mt-1">
          {/* TODO: translate below text */}
          <Tooltip
            id={`doc${document.document_id}`}
            tooltip="The years in which documents were first published"
          />
        </div>
      </div>
      <p className="text-indigo-400 mt-3">
        {truncateString(
          document.document_description.replace(/(<([^>]+)>)/gi, ''),
          250
        )}
      </p>
      {/* TODO: translate below text, how to handle plurals? */}
      {document.document_passage_matches.length > 0 && (
        <button
          className="text-indigo-500 underline text-sm mt-3 transition duration-300 hover:text-indigo-600"
          onClick={onClick}
        >
          {document.document_passage_matches.length} match
          {`${document.document_passage_matches.length === 1 ? '' : 'es'}`} in
          document
        </button>
      )}
    </div>
  );
};
export default SearchResult;
