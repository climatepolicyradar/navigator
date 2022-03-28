import { useRef } from 'react';
import Link from 'next/link';

const AccountMenu = ({ setShowMenu, logout }) => {
  return (
    <div className="absolute rounded right-0 bg-white shadow-md py-2 w-48">
      <Link href="/account">
        <a
          onClick={() => setShowMenu(false)}
          className="px-6 pb-2 block border-b border-indigo-200"
        >
          Account
        </a>
      </Link>
      <a onClick={logout} className="cursor-pointer px-6 mt-2 block">
        {' '}
        Log out
      </a>
    </div>
  );
};
export default AccountMenu;
