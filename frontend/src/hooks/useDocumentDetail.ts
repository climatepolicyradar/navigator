import { useQuery, useQueryClient } from 'react-query';
import { ApiClient } from '../api/http-common';

export default function useDocumentDetail(id: string) {
  const client = new ApiClient();

  return useQuery(
    'document_detail',
    () => client.get(`/documents/${id}`, null),

    { refetchOnWindowFocus: false, enabled: id !== undefined }
  );
}
