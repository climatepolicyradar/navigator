import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useSearch(id) {
  const client = new ApiClient('http://localhost:8000/');
  return useQuery(id, () =>
    // client.post(`/searches`, { query_string: 'test', exact_match: true })
    client.get('testdata/searches.json', null)
  );
}
