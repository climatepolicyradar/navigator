import { useEffect, useState, useRef } from 'react';
import Loader from './Loader';
import useOutsideAlerter from '../hooks/useOutsideAlerter';
import ToggleDocumentMenu from './menus/ToggleDocumentMenu';

const PassageMatches = ({ document, setShowPDF, showPDF }) => {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef();
  const { data: doc } = document;
  useOutsideAlerter(menuRef, () => setShowMenu(false));
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };
  useEffect(() => {});
  return (
    <>
      {!doc ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <div className="px-6">
          {doc.document_passage_matches.map((item) => (
            <div key={item.text_block_id} className="py-4">
              <span className="text-xs text-blue-500">
                {/* TODO: translation */}
                On page {item.text_block_page}
              </span>
              <p className="mt-2 text-indigo-400">...{item.text}...</p>
            </div>
          ))}
        </div>
      )}
    </>
  );
};
export default PassageMatches;
