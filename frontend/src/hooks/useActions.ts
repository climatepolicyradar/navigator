import { useQuery } from 'react-query';
import ApiClient from '../api/http-common';

export default function useActions(id) {
  const client = new ApiClient()
  return useQuery('actions', () =>
    client.get(`/actions?page=1&size=20`, null)
  );
}