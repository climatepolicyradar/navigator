import { useState, useRef } from 'react';
import AccountMenu from './AccountMenu';
import useOutsideAlerter from '../../hooks/useOutsideAlerter';
import { MenuIcon } from '../svg/Icons';

function ToggleAccountMenu({ logout }) {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);
  useOutsideAlerter(menuRef, () => setShowMenu(false));
  const toggleMenu = (e) => {
    e.preventDefault();
    setShowMenu(!showMenu);
  };
  return (
    <div ref={menuRef} className="ml-auto relative z-20">
      <button data-cy="menu-icon" onClick={toggleMenu}>
        <MenuIcon />
      </button>
      {showMenu && (
        <div className="absolute right-0 z-50">
          <AccountMenu setShowMenu={setShowMenu} logout={logout} />
        </div>
      )}
    </div>
  );
}
export default ToggleAccountMenu;
