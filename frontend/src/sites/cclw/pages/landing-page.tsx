import React from "react";

import Main from "../layouts/main";
import { Hero } from "../components/Hero";
import { Articles } from "../components/Articles";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  handleSearchChange: (type: string, value: any) => void;
  searchInput: string;
};

const LandingPage = ({ handleSearchInput, handleSearchChange, searchInput }: TProps) => {
  return (
    <Main>
      <Hero handleSearchInput={handleSearchInput} searchInput={searchInput} />
      <Articles />
    </Main>
  );
};

export default LandingPage;
