import { useState, useEffect } from 'react';
import TabbedNavItem from './TabbedNavItem';

interface TabbedNavProps {
  handleTabClick(e): void;
  items: string[];
  activeIndex: number;
}

const TabbedNav = ({
  handleTabClick,
  items,
  activeIndex = 0,
}: TabbedNavProps) => {
  const [activeTab, setActiveTab] = useState(activeIndex);
  const onClick = (e, index) => {
    setActiveTab(index);
    handleTabClick(e);
  };
  useEffect(() => {
    setActiveTab(activeIndex);
  }, [activeIndex]);
  return (
    <div className="grid grid-cols-2 md:grid-cols-none md:flex border-b border-blue-200 pb-2 md:pl-8">
      {items.map((item, index) => (
        <TabbedNavItem
          key={`tab${index}`}
          title={item}
          index={index}
          activeTab={activeTab}
          onClick={(e) => {
            onClick(e, index);
          }}
        />
      ))}
    </div>
  );
};
export default TabbedNav;
