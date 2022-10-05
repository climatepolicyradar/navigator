import React from "react";
import Main from "../layouts/main";
import { Hero } from "../components/Hero";
import { Articles } from "../components/Articles";
import { Partners } from "@cclw/components/Partners";

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  handleSearchChange: (type: string, value: any) => void;
  searchInput: string;
};

const LandingPage = ({ handleSearchInput, handleSearchChange, searchInput }: TProps) => {
  return (
    <Main>
      <Hero handleSearchInput={handleSearchInput} searchInput={searchInput} />
      <div className="container mt-12">
        <h2 className="text-center mb-6">Featured Content</h2>
        <Articles />
      </div>
      <div className="container mt-12">
        <h2 className="text-center mb-6">Our partners</h2>
        <Partners />
      </div>
    </Main>
  );
};

export default LandingPage;
