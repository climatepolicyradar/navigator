import { useRouter } from 'next/router';
import AccountNavItem from "./AccountNavItem";

const AccountNav = () => {
  const menu = [
    {
      title: "My Details",
      href: "/account"
    },
    {
      title: "Password",
      href: "/account/change-password"
    },
    {
      title: "Email",
      href: "/account/change-change"
    },
    {
      title: "Preferences",
      href: "/account/preferences"
    },
    {
      title: "Searches",
      href: "/account/searches"
    },
  ]
  
  const router = useRouter();
  return (
    <div className="border-b border-b-indigo-200">
      {menu.map((item, index) => (
        <AccountNavItem key={index} title={item.title} href={item.href} path={router.pathname} />
      ))}
    </div>
  )
}
export default AccountNav;