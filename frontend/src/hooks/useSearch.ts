import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { initialSearchCriteria } from '../constants/searchCriteria';

export default function useSearch(id, obj = initialSearchCriteria) {
  const client = new ApiClient();

  const config = {
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };

  const getResults = async () => {
    const results = await client.post(`/searches`, obj, config);
    return results;
  };

  return useQuery(
    id,
    () => {
      return getResults();
    },
    {
      enabled: obj.query_string.length > 0,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
      cacheTime: 1000 * 60 * 60 * 24,
    }
  );
}
