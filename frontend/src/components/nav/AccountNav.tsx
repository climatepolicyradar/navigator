import { useRouter } from 'next/router';
import AccountNavItem from './AccountNavItem';

function AccountNav() {
  /* TODO: Internationalize this menu */
  const menu = [
    {
      title: 'My Details',
      href: '/account',
    },
    {
      title: 'Change password',
      href: '/account/change-password-request',
    },
    // {
    //   title: 'Change email',
    //   href: '/account/change-email',
    // },
  ];

  const router = useRouter();
  return (
    <div className="w-full overflow-x-hidden mt-10 md:mt-20">
      <div className="border-b border-b-indigo-200 pb-4 flex no-wrap w-auto overflow-x-auto no-scrollbar">
        {menu.map((item, index) => (
          <AccountNavItem
            key={index}
            title={item.title}
            href={item.href}
            path={router.pathname}
          />
        ))}
      </div>
    </div>
  );
}
export default AccountNav;
