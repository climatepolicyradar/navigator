interface TabbedNavItemProps {
  title: string;
  index: number;
  activeTab: number;
  onClick(e: React.MouseEvent<HTMLButtonElement, MouseEvent>): void;
}

function TabbedNavItem({
  title,
  index,
  activeTab,
  onClick,
}: TabbedNavItemProps) {
  const cssClass = `text-left mt-4 md:mt-0 font-medium text-lg text-indigo-400 hover:text-blue-600 mr-8 ${
    activeTab === index ? 'tabbed-nav__active' : ''
  }`;
  return (
    <button onClick={onClick} className={cssClass}>
      {title}
    </button>
  );
}
export default TabbedNavItem;
