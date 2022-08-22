import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { removeDuplicates } from '../utils/removeDuplicates';

export default function useLookups(path: string, filterProp: string = '') {
  const client = new ApiClient();

  const modifyData = (response) => {
    let { data } = response;
    let list = data;

    if (filterProp.length) {
      list = removeDuplicates(list, filterProp);
    }
    return { ...response, data: list };
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
      return { data: { level1, level2 } };
    }
  };

  return useQuery(
    path,
    async () => {
      const response = await client.get(`/${path}`, null);
      const response_deduplicated = modifyData(response);
      const response_geo = modifyGeoData(response_deduplicated.data.geographies, 2, '');
      return { data: { response_deduplicated, response_geo }};
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
