import { useQuery } from "react-query";
import { ApiClient } from "../api/http-common";
import { TGeographySummary } from "@types";

export default function useGeoSummary(id: string) {
  const client = new ApiClient();

  const isEnabled = (parameter: any) => {
    if (typeof parameter !== "string") return false;
    if (parameter === "undefined") return false;
    return true;
  };

  return useQuery<{ data: TGeographySummary }>(
    ["geo_summary"],
    () => {
      return client.get(`/summaries/country/${id}`, null);
    },
    {
      refetchOnWindowFocus: false,
      enabled: isEnabled(id),
    }
  );
}
