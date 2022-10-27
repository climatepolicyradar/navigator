import { useQuery } from "react-query";
import { ApiClient, getEnvFromServer } from "../api/http-common";
import { initialSearchCriteria } from "../constants/searchCriteria";

export default function useSearch(id: string, obj = initialSearchCriteria) {
  const config = {
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
    },
  };

  const getResults = async () => {
    const { data } = await getEnvFromServer();
    const client = new ApiClient(data?.env?.api_url);
    const results = await client.post(`/searches`, obj, config);
    return results;
  };

  return useQuery(
    id,
    () => {
      return getResults();
    },
    {
      refetchOnWindowFocus: false,
      cacheTime: 1000 * 60 * 60 * 24,
    }
  );
}
