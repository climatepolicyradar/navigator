import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { removeDuplicates } from '../utils/removeDuplicates';
import useFilteredCountries from "@hooks/useFilteredCountries";

export default function useLookups(path: string, filterProp: string = '') {
  const client = new ApiClient();

  const modifyData = (response) => {
    let { data } = response;
    let list = data;

    if (filterProp.length) {
      list = removeDuplicates(list, filterProp);
    }
    return list;
  };

  const modifyGeoData = (response, levels, filterProp) => {
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

      console.log('level2', level2);

      const filteredCountries = useFilteredCountries(level1);
      return { level1, level2, filteredCountries };
    }
  };

  return useQuery(
    path,
    async () => {
      const response = await client.get(`/${path}`, null);
      const response_deduplicated = modifyData(response);
      const response_geo = modifyGeoData(response_deduplicated.geographies, 2, '');
      const document_types = response_deduplicated.document_types;
      const geographies = response_deduplicated.geographies;
      const instruments = response_deduplicated.instruments;
      const sectors = response_deduplicated.sectors;
      const regions = response_geo.level1;
      const countries = response_geo.level2;
      const filteredCountries = response_geo.filteredCountries;

      const resp_end = {
        document_types,
        geographies,
        instruments,
        sectors,
        regions,
        countries,
        filteredCountries
      }
      return resp_end;
    },
    {
      onSuccess: (data) => {
//         console.log(data);
      },
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      cacheTime: 1000 * 60 * 60 * 24,
    }
  );
}
