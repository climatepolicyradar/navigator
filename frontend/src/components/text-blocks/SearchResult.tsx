import { useEffect } from 'react';
import { DownloadPDFIcon, ViewDocumentCoverPageIcon } from '../Icons';
import { truncateString } from '../../helpers';

const SearchResult = ({ document, onClick }) => {
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
          {/* TODO: download pdf, open doc cover page on click */}
          <button className="text-indigo-500 hover:text-indigo-600 transition duration-300">
            <DownloadPDFIcon height="24" width="24" />
          </button>
          <button className="text-indigo-500 hover:text-indigo-600 transition duration-300 ml-2">
            <ViewDocumentCoverPageIcon height="24" width="24" />
          </button>
        </div>
      </div>

      <div className="flex text-xs text-indigo-400 mt-3">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`}
        />
        <span className="ml-2">
          {document.document_geography_english_shortname}
        </span>
        <span className="ml-6">{document.document_date}</span>
      </div>
      <p className="text-indigo-400 mt-3">
        {truncateString(document.document_description, 250)}
      </p>
      {/* TODO: translate below text, how to handle plurals? */}
      <button
        className="text-indigo-500 underline text-sm mt-3 transition duration-300 hover:text-indigo-600"
        onClick={onClick}
      >
        {document.document_passage_matches.length} match
        {`${document.document_passage_matches.length === 1 ? '' : 'es'}`} in
        document
      </button>
    </div>
  );
};
export default SearchResult;
