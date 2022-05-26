import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { removeDuplicates } from '../utils/removeDuplicates';

export default function useLookups(path: string, filterProp: string = '') {
  const client = new ApiClient();
  const lookupsQuery = useQuery(path, () => client.get(`/${path}`, null), {
    refetchOnWindowFocus: false,
    refetchOnMount: false,
  });
  const { data } = lookupsQuery;

  let list = [];
  if (data) {
    list = data?.data;
    if (filterProp.length) {
      list == removeDuplicates(list, filterProp);
    }
  }

  return { lookupsQuery, list };
}
