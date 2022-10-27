import { useQuery } from "react-query";
import { ApiClient, getEnvFromServer } from "../api/http-common";
import { removeDuplicates } from "../utils/removeDuplicates";

export default function useConfig(path: string, filterProp: string = "") {
  const extractNestedData = (response, levels, filterProp) => {
    let level1 = [];
    let level2Nested = [];
    let level2 = [];
    let data = response;
    if (data) {
      level1 = data.map((item) => {
        return item.node;
      });
      if (levels === 2) {
        level2Nested = data.map((item) => {
          return [...level2Nested, ...item.children];
        });

        level2 = level2Nested.flat().map((item) => item.node);
      }
      if (filterProp.length) {
        level1 = removeDuplicates(level1, filterProp);
        level2 = removeDuplicates(level2, filterProp);
      }

      return { level1, level2 };
    }
  };

  return useQuery(
    path,
    async () => {
      const { data } = await getEnvFromServer();
      console.log("in useConfig getResults() returns from getEnvFromServer()", data?.env?.api_url);
      const client = new ApiClient(data?.env?.api_url);
      const query_response = await client.get(`/${path}`, null);
      const response = query_response.data.metadata.CCLW;
      const response_geo = extractNestedData(response.geographies, 2, "");
      const document_types = response.document_types;
      const geographies = response.geographies;
      const instruments = response.instruments;
      const sectors = extractNestedData(response.sectors, 1, "").level1;
      const regions = response_geo.level1;
      const countries = response_geo.level2;

      const resp_end = {
        document_types,
        geographies,
        instruments,
        sectors,
        regions,
        countries,
      };
      return resp_end;
    },
    {
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      cacheTime: 1000 * 60 * 60 * 24,
    }
  );
}
