import { TDocument } from '@types';
import { useQuery, useQueryClient } from 'react-query';

export default function useDocument() {
  const queryClient = useQueryClient();
  return useQuery<TDocument>(
    'document',
    (): TDocument => {
      const document: TDocument = queryClient.getQueryData('document');
      return document ? document : null;
    },
    {
      refetchOnWindowFocus: false,
    }
  );
}
