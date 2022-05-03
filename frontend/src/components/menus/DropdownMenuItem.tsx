import Link from 'next/link';

interface DropdownMenuItemProps {
  first?: boolean;
  title: string;
  href?: string;
  onClick?(): void;
  setShowMenu?(value: boolean): void;
}
const DropdownMenuItem = ({
  first = false,
  title,
  href,
  onClick = () => {},
  setShowMenu,
}: DropdownMenuItemProps) => {
  const cssClass = `${
    !first ? 'border-t border-indigo-200 pt-3' : 'pt-2'
  } px-6 pt-2 block w-full text-left text-sm pb-3 hover:text-blue-500 transition duration-300`;
  const handleClick = () => {
    onClick();
    setShowMenu(false);
  };
  return (
    <>
      {href ? (
        <Link href={href}>
          <a onClick={handleClick} className={cssClass}>
            {title}
          </a>
        </Link>
      ) : (
        <button className={cssClass} onClick={handleClick}>
          {title}
        </button>
      )}
    </>
  );
};
export default DropdownMenuItem;
