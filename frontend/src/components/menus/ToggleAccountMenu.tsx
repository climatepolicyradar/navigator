import { useState, useRef } from 'react';
import AccountMenu from '../menus/AccountMenu';
import useOutsideAlerter from '../../hooks/useOutsideAlerter';
import { MenuIcon } from '../Icons';

const ToggleAccountMenu = ({ logout }) => {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);
  useOutsideAlerter(menuRef, () => setShowMenu(false));
  const toggleMenu = (e) => {
    e.preventDefault();
    setShowMenu(!showMenu);
  };
  return (
    <div ref={menuRef} className="ml-auto relative">
      <button data-cy="menu-icon" onClick={toggleMenu}>
        <MenuIcon />
      </button>
      {showMenu && <AccountMenu setShowMenu={setShowMenu} logout={logout} />}
    </div>
  );
};
export default ToggleAccountMenu;
