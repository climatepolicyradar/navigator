import Main from "../layouts/main";
import LandingSearchForm from "@components/forms/LandingSearchForm";

const LandingPage = () => {
  return (
    <Main>
      <h2>CCLW Landing Page</h2>
      <LandingSearchForm placeholder="CCLW search placeholder" handleSearchInput={() => {}} />
    </Main>
  );
};

export default LandingPage;
