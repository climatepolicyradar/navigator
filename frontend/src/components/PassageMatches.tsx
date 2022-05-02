import { useEffect } from 'react';
import Kebab from './buttons/Kebab';
import Loader from './Loader';
import useOutsideAlerter from '../hooks/useOutsideAlerter';

const PassageMatches = ({ document }) => {
  const { data: doc } = document;
  // useOutsideAlerter(menuRef, () => setShowMenu(false));
  const toggleMenu = () => {};
  useEffect(() => {});
  return (
    <>
      {!doc ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <div>
          {/* {console.log(document.data)} */}
          <div className="border-b border-blue-200 pb-4 flex justify-between">
            <div className="pl-4 pr-6 mt-2">
              <h1 className="text-lg text-blue-500 font-medium">
                {doc.document_name}
              </h1>
              {/* TODO: translate below text, how to handle plurals? */}
              <p className="text-indigo-500 text-sm">
                {doc.document_passage_matches.length}{' '}
                {`match${
                  doc.document_passage_matches.length === 1 ? '' : 'es'
                }`}{' '}
                in document.
              </p>
            </div>
            <div className="flex-shrink-0 mr-4">
              <Kebab onClick={toggleMenu} />
            </div>
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
