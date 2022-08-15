import { useQuery } from "react-query";
import { ApiClient } from "../api/http-common";
import { TCountryAPI } from "@types";

export default function useGeoStats(id: string) {
  const client = new ApiClient();

  return useQuery<TCountryAPI>(
    ["geo_stats"],
    () => {
      return client.get(`/geo_stats/${id}`, null);
    },
    {
      refetchOnWindowFocus: false,
      enabled: id !== undefined,
    }
  );
}
