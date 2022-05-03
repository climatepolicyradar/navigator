import { useState, useRef } from 'react';
import useOutsideAlerter from '../../hooks/useOutsideAlerter';
import Kebab from '../buttons/Kebab';
import DocumentMenu from './DocumentMenu';

const ToggleDocumentMenu = () => {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);
  useOutsideAlerter(menuRef, () => setShowMenu(false));
  const toggleMenu = (e) => {
    e.preventDefault();
    setShowMenu(!showMenu);
  };
  return (
    <div ref={menuRef} className="flex-shrink-0 mr-4">
      <Kebab onClick={toggleMenu} />
      <div
        className={`${
          !showMenu ? 'hidden' : ''
        } absolute top-0 right-0 mt-12 mr-4 z-50`}
      >
        <DocumentMenu setShowMenu={setShowMenu} />
      </div>
    </div>
  );
};
export default ToggleDocumentMenu;
