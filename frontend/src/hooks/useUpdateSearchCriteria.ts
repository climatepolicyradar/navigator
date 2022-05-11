import { useMutation, useQueryClient } from 'react-query';

export default function useUpdateSearchCriteria() {
  const queryClient = useQueryClient();

  return useMutation(
    (value: any) => {
      return queryClient.setQueryData('searchCriteria', (old) => ({
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
