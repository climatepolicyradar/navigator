import { TGeography } from "@types";


const findCountryObject = (countrySearch: string, dataSet: TGeography[]) => {
  let country = dataSet.find((c) => c.value.toLowerCase() === countrySearch.toLowerCase());
  if (!country) country = dataSet.find((c) => c.display_value.toLowerCase() === countrySearch.toLowerCase());
  if (!country) country = dataSet.find((c) => c.slug.toLowerCase() === countrySearch.toLowerCase());
  if (!country) return null;
  return country;
};

export const getCountrySlug = (countrySearch: string, dataSet: TGeography[]) => {
  return findCountryObject(countrySearch, dataSet)?.slug;
};

export const getCountryName = (countrySearch: string, dataSet: TGeography[]) => {
  return findCountryObject(countrySearch, dataSet)?.display_value;
};
