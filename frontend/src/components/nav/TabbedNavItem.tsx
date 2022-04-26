interface TabbedNavItemProps {
  title: string;
  index: number;
  activeTab: number;
  onClick(e): void;
}

const TabbedNavItem = ({
  title,
  index,
  activeTab,
  onClick,
}: TabbedNavItemProps) => {
  const cssClass = `font-medium text-lg text-indigo-400 hover:text-blue-500 mr-8 ${
    activeTab === index ? 'category-active' : ''
  }`;
  return (
    <button onClick={onClick} className={cssClass}>
      {title}
    </button>
  );
};
export default TabbedNavItem;
