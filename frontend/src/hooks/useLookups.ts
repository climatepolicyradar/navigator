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
  return useQuery(
    path,
    async () => {
      const response = await client.get(`/${path}`, null);
      return modifyData(response);
    },
    {
       refetchOnWindowFocus: false,
       refetchOnMount: false,
       cacheTime: 1000 * 60 * 60 * 24,
    }
  );
}
