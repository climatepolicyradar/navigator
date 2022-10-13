import { ApiClient } from "@api/http-common";
import { TGeographyConfig } from "@types";

function Sitemap() {}


function getGeographyIdsFromConfig(config: TGeographyConfig) {
  //config.reduce
}

export async function getServerSideProps({ res }) {
  const client = new ApiClient();

  const {data: data} = await client.get(`/config/`, null);
  console.log(data);
  console.log("-----");

  const geographyData: TGeographyConfig = data.metadata.CCLW.geographies;
  console.log(geographyData);

  res.setHeader("Content-Type", "text/plan");
  res.write(JSON.stringify(geographyData, null, 4));
  res.end();

  return {
    props: {},
  };
}

export default Sitemap;
