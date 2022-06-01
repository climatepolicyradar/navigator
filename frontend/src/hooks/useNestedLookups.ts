import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { removeDuplicates } from '../utils/removeDuplicates';

export default function useNestedLookups(path, filterProp = '', levels = 1) {
  /*
  path: the path / name of the collection
  filterProp: if we are filtering out duplicates, the property to filter on (assuming it's the same on all levels)
  levels: how many levels deep is the nesting (currently only 1 or 2)
  */

  /* assuming the data structure is:
  data: [
    {
      node: {
      ..properties
      },
      children: [
        {
          node: {
            ...properties
          },
          children: []
        }
      ]
  }
  ]
  */

  const client = new ApiClient();

  const modifyData = (response) => {
    let { data } = response;
    let level1 = [];
    let level2Nested = [];
    let level2 = [];
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
      return { ...response, data: { level1, level2 } };
    }
  };

  return useQuery(
    path,
    async () => {
      const response = await client.get(`/${path}`, null);
      return modifyData(response);
    },
    {
      onSuccess: (data) => {
        // console.log(data);
      },
      refetchOnWindowFocus: false,
      refetchOnMount: false,
    }
  );
}
