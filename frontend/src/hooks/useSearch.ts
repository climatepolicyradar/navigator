import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { fakePromise } from '../helpers';

export default function useSearch(id, obj = null) {
  const client = new ApiClient('http://localhost:3000/'); // note: remove baseUrl argument when api is finally ready
  const fake = async () => {
    // get dummy data with latency added
    const value = await client.get('testdata/searches.json', obj);
    return fakePromise(500, value);
  };

  return useQuery(
    id,
    () =>
      // client.post(`/searches`, { query_string: 'test', exact_match: true })
      fake(),
    // client.get('testdata/searches.json', obj),
    { refetchOnWindowFocus: false }
  );
}
