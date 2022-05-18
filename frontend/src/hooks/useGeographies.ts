import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useGeographies(filter = null) {
  const client = new ApiClient();
  const geosQuery = useQuery('geographies', () =>
    client.get(`/geographies`, null)
  );
  const { data } = geosQuery;
  let arr = [];
  let geographies = [];
  if (data) {
    arr = data?.data.map((item) => {
      return [...arr, ...item.children];
    });
    geographies = arr.flat().map((item) => item.node);
  }

  return { geosQuery, geographies };
}
