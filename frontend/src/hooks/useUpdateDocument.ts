import { useQuery, useMutation, useQueryClient } from 'react-query';
import { v4 as uuidv4 } from 'uuid';

export default function useUpdateDocument() {
  const queryClient = useQueryClient();

  return useMutation((value) => {
    const {
      data: { documents },
    }: any = queryClient.getQueryData('searches');
    const id = Number(value);
    const document = documents.find((item) => item.document_id === id);
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
