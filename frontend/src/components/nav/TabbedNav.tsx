import { useState } from 'react';
import TabbedNavItem from './TabbedNavItem';

interface TabbedNavProps {
  handleTabClick(e): void;
  items: string[];
}

const TabbedNav = ({ handleTabClick, items }: TabbedNavProps) => {
  const [activeTab, setActiveTab] = useState(0);
  const onClick = (e, index) => {
    setActiveTab(index);
    handleTabClick(e);
  };
  return (
    <div className="border-b border-blue-200 pb-2 pl-8">
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
