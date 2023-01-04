import React from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { Hero } from "../components/Hero";
import { Articles } from "../components/Articles";
import { Partners } from "@cclw/components/Partners";

import dynamic from "next/dynamic";

const Map = dynamic(() => import("@components/map/Map"), {
  ssr: false,
});

type TProps = {
  handleSearchInput: (term: string, filter?: string, filterValue?: string) => void;
  searchInput: string;
};

const LandingPage = ({ handleSearchInput, searchInput }: TProps) => {
  return (
    <>
      <Map />
      <main className="flex flex-col flex-1">
        <div className="gradient-container">
          <Header background={false} />
          <Hero handleSearchInput={handleSearchInput} searchInput={searchInput} />
        </div>
        <div className="container mt-12">
          <h2 className="text-center mb-6">Featured Content</h2>
          <Articles />
        </div>
        <div className="container mt-12">
          <h2 className="text-center mb-6">Our partners</h2>
          <Partners />
        </div>
      </main>
      <Footer />
    </>
  );
};

export default LandingPage;
