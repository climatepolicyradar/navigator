import Link from 'next/link';

interface AccountNavItemProps {
  href: string;
  path: string;
  title: string;
}
function AccountNavItem({ href, path, title }: AccountNavItemProps) {
  return (
    <Link href={href} passHref>
      <a
        className={`${
          href === path ? 'subnav-active text-blue-600' : ''
        } hover:text-blue-600 transition duration-300 mr-3 md:mr-5 flex-shrink-0`}
      >
        {title}
      </a>
    </Link>
  );
}
export default AccountNavItem;
