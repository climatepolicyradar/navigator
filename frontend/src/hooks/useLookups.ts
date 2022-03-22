import { useQuery } from 'react-query';
import ApiClient from '../api/http-common';

export default function useLookups(path) {
  const client = new ApiClient()
  return useQuery(path, () =>
    client.get(`/${path}`, null)
  );
}
