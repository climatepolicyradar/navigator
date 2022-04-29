import { useQuery, useMutation, useQueryClient } from 'react-query';

export default function useUpdateDocument() {
  const queryClient = useQueryClient();

  return useMutation((value) => {
    const { documents } = queryClient.getQueryData('searches');
    const document = documents.find((item) => item.document_id === value);
    return queryClient.setQueryData('document', (old) => {
      return {
        ...old,
        ...document,
      };
    });
  });
}
