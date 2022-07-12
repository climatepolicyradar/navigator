import { useMutation, useQueryClient } from 'react-query';

export default function useUpdateSearch() {
  const queryClient = useQueryClient();

  return useMutation(
    (value: any) => {
      return queryClient.setQueryData('searches', (old) => ({
        ...old,
        ...value,
      }));
    },

    {
      onError: (err) => {
        console.log(err);
      },
    }
  );
}
