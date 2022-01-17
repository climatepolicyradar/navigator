import { useEffect, useState, useRef } from 'react';
import Logo from '../Logo';
import Link from 'next/link';

const Header = () => {
  const [fixed, setFixed] = useState(false);

  const headerRef = useRef(null);

  useEffect(() => {
    document.addEventListener('scroll', function (e) {
      if (window.scrollY > 70) {
        setFixed(true);
      } else {
        setFixed(false);
      }
    });
  }, []);
  return (
    <header
      ref={headerRef}
      className={`${
        fixed ? 'fixed bg-sky' : 'absolute bg-transparent'
      } w-full top-0 left-0 transition duration-300`}
    >
      <div className="container my-4">
        <div>
          <span className={`${fixed ? 'text-indigo-600' : 'text-white'}`}>
            <Link href="/">
              <a>
                <Logo fixed={fixed} />
              </a>
            </Link>
          </span>
        </div>
      </div>
    </header>
  );
};
export default Header;
