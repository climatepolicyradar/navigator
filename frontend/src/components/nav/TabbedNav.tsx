import { useState, useEffect } from "react";
import TabbedNavItem from "./TabbedNavItem";

interface TabbedNavProps {
  handleTabClick(e: React.MouseEvent<HTMLButtonElement, MouseEvent>): void;
  items: string[];
  activeIndex: number;
  showBorder?: boolean;
}

const TabbedNav = ({ handleTabClick, items, activeIndex = 0, showBorder = true }: TabbedNavProps) => {
  const [activeTab, setActiveTab] = useState(activeIndex);

  useEffect(() => {
    setActiveTab(activeIndex);
  }, [activeIndex]);

  const onClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>, index: number) => {
    setActiveTab(index);
    handleTabClick(e);
  };

  return (
    <div className={`grid grid-cols-2 md:grid-cols-none md:flex pb-2 md:pl-8 ${showBorder && 'border-b border-blue-200'}`}>
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
