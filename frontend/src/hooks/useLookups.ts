import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useLookups(path: string, filter = null) {
  // const client = new ApiClient();
  // const results = useQuery(path, () => client.get(`/${path}`, null));
  // note: use above 2 lines instead of below 2 lines when lookups api is back!
  const client = new ApiClient('http://localhost:8000/');
  const results = useQuery(
    path,
    () => client.get(`testdata/${path}.json`, null) // dummy data
  );

  if (filter) {
    // TODO: filter the results based on some filter that is passed in
    return results;
  }
  return results;
}
