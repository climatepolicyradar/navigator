import { useQuery, useQueryClient } from 'react-query';

export default function useDocument() {
  const queryClient = useQueryClient();
  return useQuery(
    'document',
    () => {
      const document = queryClient.getQueryData('document');
      return document ? document : null;
    },
    {
      refetchOnWindowFocus: false,
    }
  );
}
