import Link from "next/link";

const AccountNavItem = ({href, path, title}) => {
  return (
    <Link href={href} passHref>
      <a className={`${href === path ? 'text-blue-500' : ''} font-medium mr-2`}>
        {title}
      </a>
    </Link>
  )
}
export default AccountNavItem;