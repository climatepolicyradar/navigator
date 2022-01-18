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
      data-cy="header"
      ref={headerRef}
      className={`${
        fixed ? 'fixed bg-sky' : 'absolute bg-transparent'
      } w-full top-0 left-0 transition duration-300 z-10`}
    >
      <div className="container my-4">
        <div className="flex items-start">
          <span className={`${fixed ? 'text-indigo-600' : 'text-white'}`}>
            <Link href="/">
              <a>
                <Logo fixed={fixed} />
              </a>
            </Link>
          </span>
          <div data-cy="product-name" className="flex items-start">
            <h1
              className={`${
                fixed
                  ? 'text-indigo-600 text-2xl md:text-4xl'
                  : 'text-white text-2xl md:text-5xl'
              } ml-6 md:ml-8 text-white tracking-wider leading-none transition-all duration-300`}
            >
              Navigator
            </h1>
            <span
              data-cy="alpha"
              className="bg-yellow-500 ml-2 mt-2 text-xs text-indigo-600 px-1 rounded"
            >
              alpha
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};
export default Header;
