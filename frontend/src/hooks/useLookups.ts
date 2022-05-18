import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useLookups(path: string) {
  const client = new ApiClient();
  const lookupsQuery = useQuery(path, () => client.get(`/${path}`, null));
  const { data } = lookupsQuery;

  // filter for dupes
  let filteredList = [];
  if (data) {
    filteredList = data?.data.filter((item) => {
      // return [...arr, ...item.children];
    });
  }

  return { lookupsQuery, filteredList };
}
