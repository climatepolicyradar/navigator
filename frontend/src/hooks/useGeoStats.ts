import { useQuery } from "react-query";
import { ApiClient } from "../api/http-common";
import { TGeographyStats } from "@types";

export default function useGeoStats(id: string) {
  const client = new ApiClient();

  const isEnabled = (parameter: any) => {
    if (typeof parameter !== "string") return false;
    if (parameter === "undefined") return false;
    return true;
  };

  return useQuery<{ data: TGeographyStats }>(
    ["geo_stats"],
    () => {
      return client.get(`/geo_stats/${id}`, null);
    },
    {
      refetchOnWindowFocus: false,
      enabled: isEnabled(id),
    }
  );
}
