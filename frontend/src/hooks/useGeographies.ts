import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useGeographies() {
  const client = new ApiClient();
  const results = useQuery('geographies', () =>
    client.get(`/geographies`, null)
  );
  // note: use above 2 lines instead of below 2 lines when lookups api is back!
  // const client = new ApiClient('http://localhost:3000/');
  // const results = useQuery(
  //   path,
  //   () => client.get(`testdata/${path}.json`, null) // dummy data
  // );

  // const regions =
  return results;
}
