import { useMutation, useQueryClient } from 'react-query';
import { ApiClient } from '../api/http-common';

const useUpdateAccount = () => {
  const client = new ApiClient();
  const queryClient = useQueryClient();
  return useMutation((values) => client.put('/users/me', values), {
    onSuccess: (data: any) => {
      queryClient.setQueryData('auth-user', data.data);
    },
    onError: (err) => {
      console.log(err);
    },
    onSettled: () => {
      window.scrollTo(0, 0);
    },
  });
};

export default useUpdateAccount;
