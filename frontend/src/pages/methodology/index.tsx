import Layout from "@components/layouts/Main";
// import getSite from "@utils/getSite";

import CPRMethodology from "@cpr/pages/methodology";
import CCLWMethodology from "@cclw/pages/methodology";

import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";

const Methodology = () => {
  // const site = getSite();
  const theme = useContext(ThemeContext);

  return (
    <Layout title={"Methodology"}>
      {theme === "cpr" && <CPRMethodology />}
      {theme === "cclw" && <CCLWMethodology />}
    </Layout>
  );
};
export default Methodology;
