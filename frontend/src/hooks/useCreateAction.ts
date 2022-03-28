import { ApiClient } from '../api/http-common';
import { storage } from '../utils/storage';
import { useMutation, useQueryClient } from 'react-query';

const useCreateAction = () => {
  const queryClient = useQueryClient();
  const client = new ApiClient();
  return useMutation((values) => client.post(`/actions`, values), {
    onError: (err) => {
      console.log(err);
    },
    onSettled: () => {
      window.scrollTo(0, 0);
    },
  });
};

export default useCreateAction;
