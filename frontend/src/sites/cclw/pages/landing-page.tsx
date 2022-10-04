import React from "react";
import Main from "../layouts/main";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  handleSearchChange: (type: string, value: any) => void;
  searchInput: string;
};

const LandingPage = ({ handleSearchInput, handleSearchChange, searchInput }: TProps) => {
  const handleDocumentBrowseClick = (e: React.MouseEvent, category: string) => {
    e.preventDefault();
    handleSearchInput("", "categories", category);
  };

  return (
    <Main>
      <div className="bg-secondary-700 py-4 text-white">
        <div className="container">
          <a onClick={(e) => handleDocumentBrowseClick(e, "Policy")}>Policy click</a>
          <a onClick={(e) => handleDocumentBrowseClick(e, "Law")}>Law click</a>
        </div>
      </div>
    </Main>
  );
};

export default LandingPage;
