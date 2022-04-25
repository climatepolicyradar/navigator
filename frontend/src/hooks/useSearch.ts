import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useSearch(id, obj = null) {
  const client = new ApiClient('http://localhost:3000/'); // note: remove baseUrl argument when api is finally ready

  return useQuery(
    id,
    () =>
      // client.post(`/searches`, { query_string: 'test', exact_match: true })
      client.get('testdata/searches.json', obj), // dummy data
    { refetchOnWindowFocus: false }
  );
}
