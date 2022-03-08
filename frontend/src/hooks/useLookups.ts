import axios from 'axios';
import { storage } from '../utils/storage';
import { useQuery } from 'react-query';

// const headers = {
//   Authorization: `Bearer ${storage.getToken()}`,
//   'Content-Type': 'multipart/form-data',
// };
export default function useLookups(path) {
  return useQuery(path, () =>
    axios
      .get(`${process.env.NEXT_PUBLIC_API_URL}/${path}`, {
        headers: {
          Authorization: `Bearer ${storage.getToken()}`,
        },
      })
      .then((res) => res.data)
  );
}
