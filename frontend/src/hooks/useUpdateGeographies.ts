import { useMutation, useQueryClient } from 'react-query';

export default function useUpdateSearchCriteria() {
  const queryClient = useQueryClient();

  return useMutation(
    (value: any) => {
      const prev: any = queryClient.getQueryData('geographies');
      const newList = prev.filter((item: any) => item.parent_id === value.id);
      // return queryClient.setQueryData(newList)
      return queryClient.setQueryData('geographies', (old) => ({
        ...old,
        ...newList,
      }));
    },

    {
      onError: (err) => {
        console.log(err);
      },
    }
  );
}
