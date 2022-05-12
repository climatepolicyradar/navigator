import Link from 'next/link';
import LargeLogo from '../svg/LargeLogo';
import Logo from '../svg/Logo';

const AlphaLogo = () => {
  return (
    <div className="text-white flex mr-10">
      <Link href="/">
        <a className="relative block">
          <LargeLogo />
          <span
            data-cy="alpha"
            className="mt-6 md:mt-3 lg:mt-4 bg-yellow-500 ml-2 text-xs text-indigo-600 px-1 rounded absolute right-0 bottom-0 -mr-4"
          >
            alpha
          </span>
        </a>
      </Link>
    </div>
  );
};
export default AlphaLogo;
