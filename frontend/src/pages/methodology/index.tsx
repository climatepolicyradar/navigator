import { useContext } from "react";
import Layout from "@components/layouts/Main";
import { ThemeContext } from "@context/ThemeContext";

import CPRMethodology from "@cpr/pages/methodology";
import CCLWMethodology from "@cclw/pages/methodology";


const Methodology = () => {
  const theme = useContext(ThemeContext);

  return (
    <Layout title={"Methodology"}>
      {theme === "cpr" && <CPRMethodology />}
      {theme === "cclw" && <CCLWMethodology />}
    </Layout>
  );
};
export default Methodology;
