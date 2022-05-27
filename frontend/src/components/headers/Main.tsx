import { useEffect, useState, useRef } from 'react';
import Logo from '../svg/Logo';
import Link from 'next/link';
import ProductName from '../ProductName';
import { useAuth } from '../../api/auth';
import ToggleAccountMenu from '../menus/ToggleAccountMenu';
import AlphaLogoSmall from '../logo/AlphaLogoSmall';

const Header = () => {
  const [fixed, setFixed] = useState(false);
  const { logout } = useAuth();
  const headerRef = useRef(null);

  useEffect(() => {}, []);
  return (
    <header
      data-cy="header"
      ref={headerRef}
      className={`${
        fixed ? 'fixed bg-sky' : 'absolute bg-transparent'
      } w-full top-0 left-0 transition duration-300 z-10`}
    >
      <div className="container my-4">
        <div className="flex items-start justify-between">
          <AlphaLogoSmall />

          <div>
            <ToggleAccountMenu logout={logout} />
          </div>
        </div>
      </div>
    </header>
  );
};
export default Header;
