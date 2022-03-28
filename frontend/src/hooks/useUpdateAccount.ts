import { ApiClient } from '../api/http-common';
import { useMutation } from 'react-query';

const useUpdateAccount = () => {
  const client = new ApiClient();

  return useMutation((values) => client.put(`/users/${values.id}`, values), {
    onError: (err) => {
      console.log(err);
    },
    onSettled: () => {
      window.scrollTo(0, 0);
    },
  });
};

export default useUpdateAccount;
