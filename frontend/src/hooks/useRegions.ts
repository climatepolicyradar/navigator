import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useRegions() {
  const client = new ApiClient();
  const regionsQuery = useQuery('regions', () =>
    client.get(`/geographies`, null)
  );
  const { data } = regionsQuery;

  let arr = [];
  let regions = [];
  if (data) {
    regions = data?.data.map((item) => {
      // console.log(item.node);
      return item.node;
    });
    // regions = arr.map((item) => item.node);
    // console.log(arr);
  }

  return { regionsQuery, regions };
}
