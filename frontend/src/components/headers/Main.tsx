import { useEffect, useState, useRef } from 'react';
import Logo from '../Logo';
import Link from 'next/link';
import ProductName from '../ProductName';
import { useAuth } from '../../api/auth';
import ToggleAccountMenu from '../menus/ToggleAccountMenu';

const Header = () => {
  const [fixed, setFixed] = useState(false);
  const { logout } = useAuth();
  const headerRef = useRef(null);

  useEffect(() => {
    document.addEventListener('scroll', function (e) {
      if (window.scrollY > 70) {
        setFixed(false);
      } else {
        setFixed(false);
      }
    });
  }, []);
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
          <span className={`${fixed ? 'text-indigo-600' : 'text-white'}`}>
            <Link href="https://climatepolicyradar.org">
              <a>
                <Logo fixed={fixed} />
              </a>
            </Link>
          </span>
          <div className="hidden md:block">
            <ProductName fixed={fixed} />
          </div>
          <div>
            <ToggleAccountMenu logout={logout} />
            {/* <button data-cy="user-icon">
              <img
                className={`${
                  fixed ? 'w-3/4' : 'w-full'
                } transtion-all duration-300`}
                src="/images/user.svg"
                alt="My account"
              />
            </button> */}
          </div>
        </div>
        {/* Mobile only */}
        <div className="md:hidden">
          <ProductName fixed={fixed} />
        </div>
      </div>
    </header>
  );
};
export default Header;
