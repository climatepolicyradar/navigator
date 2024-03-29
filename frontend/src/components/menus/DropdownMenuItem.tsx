import { ExternalLink } from "@components/ExternalLink";
import Link from "next/link";

interface DropdownMenuItemProps {
  first?: boolean;
  title: string;
  href?: string;
  target?: string;
  external?: boolean;
  onClick?(): void;
  setShowMenu?(value: boolean): void;
}
const DropdownMenuItem = ({ first = false, title, href, target = "", external = false, onClick = () => {}, setShowMenu }: DropdownMenuItemProps) => {
  const cssClass = `${!first ? "border-t border-indigo-200 pt-3" : "pt-2"} px-6 pt-2 block w-full text-left text-sm pb-3 hover:text-blue-500 transition duration-300`;
  const handleClick = () => {
    onClick();
    setShowMenu(false);
  };

  if (external)
    return (
      <ExternalLink url={href} className={cssClass}>
        {title}
      </ExternalLink>
    );

  return <>
    {href ? (
      (<Link href={href} onClick={handleClick} target={target} className={cssClass}>

        {title}

      </Link>)
    ) : (
      <button className={cssClass} onClick={handleClick}>
        {title}
      </button>
    )}
  </>;
};
export default DropdownMenuItem;
