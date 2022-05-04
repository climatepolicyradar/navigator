import { useQuery, useMutation, useQueryClient } from 'react-query';
import { v4 as uuidv4 } from 'uuid';

export default function useUpdateDocument() {
  const queryClient = useQueryClient();

  return useMutation((value) => {
    const { documents } = queryClient.getQueryData('searches');
    const document = documents.find((item) => item.document_id === value);
    // add fileid for Adobe PDF embed
    const newDocument = { ...document, document_fileid: uuidv4() };
    return queryClient.setQueryData('document', (old) => {
      return {
        ...old,
        ...newDocument,
      };
    });
  });
}
