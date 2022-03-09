import apiClient from '../api/http-common';
import { storage } from '../utils/storage';
import { useMutation, useQueryClient } from 'react-query';

const useCreateAction = () => {
  const queryClient = useQueryClient();
  return useMutation(
    (values) =>
      apiClient
        .post(`/action`, values, {
          headers: {
            Authorization: `Bearer ${storage.getToken()}`,
          },
        })
        .then((res) => res.data),
    {
      onSettled: () => {
        window.scrollTo(0, 0);
      },
    }
  );
};

export default useCreateAction;
