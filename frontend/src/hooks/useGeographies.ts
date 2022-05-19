import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useGeographies(filter = null) {
  const client = new ApiClient();
  const geosQuery = useQuery('geographies', () =>
    client.get(`/geographies`, null)
  );
  const { data } = geosQuery;
  let regions = [];
  let geosNested = [];
  let countries = [];
  if (data) {
    regions = data?.data.map((item) => {
      return item.node;
    });
    geosNested = data?.data.map((item) => {
      return [...geosNested, ...item.children];
    });

    countries = geosNested.flat().map((item) => item.node);
  }

  return { geosQuery, regions, countries };
}
