import { ApiClient } from "@api/http-common";
import { TGeographyConfig } from "@types";

function Sitemap() { }

function extractGeographyIds(config: TGeographyConfig): number[] {
  const children_ids: number[] = config.children.flatMap((node): number[] => (extractGeographyIds(node)));
  return [config.node.id].concat(children_ids);
}

async function fetchGeographies(): Promise<TGeographyConfig[]> {
  const client = new ApiClient();
  const { data: data } = await client.get(`/config/`, null);
  return data.metadata.CCLW.geographies;
}

async function getGeographyIds(): Promise<number[]> {
  const geographyData: TGeographyConfig[] = await fetchGeographies();
  return geographyData.flatMap((item: TGeographyConfig) => extractGeographyIds(item));
}

async function getGeographyPages(res: any): Promise<string[]> {
  const id_list: number[] = await getGeographyIds();
  return id_list.map((geo_id: number) => `https://app.climatepolicyradar.org/geographies/${geo_id}`);
}

export async function getServerSideProps({ res }) {

  res.setHeader("Content-Type", "text/plain");
  res.write((await getGeographyPages(res)).join('\n'));
  res.end();

  return {
    props: {},
  };

}

export default Sitemap;
