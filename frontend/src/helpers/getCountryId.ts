import { TGeography } from "@types";

export const getCountryId = (countrySearch: string, dataSet: TGeography[]) => {
  let country = dataSet.find((c) => c.value.toLowerCase() === countrySearch.toLowerCase());
  if (!country) country = dataSet.find((c) => c.display_value.toLowerCase() === countrySearch.toLowerCase());
  if (!country) return null;
  return country.id;
};
