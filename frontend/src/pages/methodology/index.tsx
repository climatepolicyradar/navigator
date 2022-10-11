import Layout from "@components/layouts/Main";
import getSite from "@utils/getSite";

import CPRMethodology from "@cpr/pages/methodology";
import CCLWMethodology from "@cclw/pages/methodology";

const Methodology = () => {
  const site = getSite();

  return (
    <Layout title={"Methodology"}>
      {site === "cpr" && <CPRMethodology />}
      {site === "cclw" && <CCLWMethodology />}
    </Layout>
  );
};
export default Methodology;
