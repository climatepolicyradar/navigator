import Image from 'next/image';
import { useEffect } from 'react';

const SearchResult = ({ document, onClick }) => {
  useEffect(() => {
    console.log(document);
  }, []);
  return (
    <div>
      <h2 className="text-left">
        <button
          onClick={onClick}
          className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight"
        >
          {document.document_name}
        </button>
      </h2>
      <div className="flex text-xs text-indigo-400 mt-3">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`}
        />
        <span className="ml-2">
          {document.document_geography_english_shortname}
        </span>
        <span className="ml-6">{document.document_date}</span>
      </div>
      <p className="text-indigo-400 mt-3">{document.document_description}</p>
      <button
        className="text-indigo-500 underline text-sm mt-3"
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
