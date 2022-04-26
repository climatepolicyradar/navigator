import { useState } from 'react';
import DocumentCategoryItem from './DocumentCategoryItem';

const DocumentCategories = ({ handleFilterChange }) => {
  const [activeTab, setActiveTab] = useState(0);
  const categories = ['All', 'Executive', 'Legislative', 'Litigation'];
  const handleClick = (e, index) => {
    setActiveTab(index);
    const val = e.currentTarget.textContent;
    const action = val === 'All' ? 'delete' : 'update';
    handleFilterChange('document_category', val, action);
  };
  return (
    <div className="border-b border-blue-200 pb-2 pl-8">
      {categories.map((item, index) => (
        <DocumentCategoryItem
          title={item}
          index={index}
          activeTab={activeTab}
          onClick={(e) => {
            handleClick(e, index);
          }}
        />
      ))}
    </div>
  );
};
export default DocumentCategories;
