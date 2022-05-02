import { useEffect } from 'react';
import Loader from './Loader';

const PassageMatches = ({ document }) => {
  const { data: doc } = document;
  useEffect(() => {});
  return (
    <>
      {!doc ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <div>
          {console.log(document.data)}
          <div className="border-b border-blue-200 pb-4">
            <h1 className="text-lg text-blue-500 font-medium px-4">
              {doc.document_name}
            </h1>
            {/* TODO: translate below text, how to handle plurals? */}
            <p className="px-4 text-indigo-500 text-sm">
              {doc.document_passage_matches.length}{' '}
              {`match${doc.document_passage_matches.length === 1 ? '' : 'es'}`}{' '}
              in document.
            </p>
          </div>

          <div className="px-4">
            {doc.document_passage_matches.map((item) => (
              <div key={item.text_block_id} className="py-4">
                <span className="text-xs text-blue-500">
                  On page {item.text_block_page}
                </span>
                <p className="mt-2 text-indigo-400">...{item.text}...</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
};
export default PassageMatches;
