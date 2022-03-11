import { useQuery } from 'react-query';
import apiClient from '../api/http-common';
import { storage } from '../utils/storage';

export default function useLookups(path) {
  return useQuery(path, () =>
    apiClient
      .get(`/${path}`, {
        headers: {
          Authorization: `Bearer ${storage.getToken()}`,
        },
      })
      .then((res) => res.data)
  );
}
