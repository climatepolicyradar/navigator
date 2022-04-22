import { useMutation, useQueryClient } from 'react-query';

export default function useUpdateSearchCriteria() {
  const queryClient = useQueryClient();

  const getKeyAndValue = (obj) => {
    const key = Object.keys(obj)[0];
    const val = Object.values(obj)[0];
    return [key, val];
  };

  return useMutation(
    (value) => {
      const prev = queryClient.getQueryData('searchCriteria');
      const [key, val] = getKeyAndValue(value);
      return queryClient.setQueryData('searchCriteria', (old) => ({
        ...old,
        [key]: val,
      }));
    },

    {
      onError: (err) => {
        console.log(err);
      },
    }
  );
}
