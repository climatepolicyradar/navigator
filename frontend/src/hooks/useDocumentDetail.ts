import { useQuery, useQueryClient } from 'react-query';
import { fakePromise } from '../helpers';
import { ApiClient } from '../api/http-common';

export default function useDocumentDetail(id: string) {
  const client = new ApiClient(); // note: remove baseUrl argument when api is finally ready
  // const fake = async () => {
  //   // get dummy data with latency added
  //   const value = await client.get('testdata/document.json', id);
  //   return fakePromise(500, value);
  // };

  return useQuery(
    'document_detail',
    () => client.get(`/documents/${id}`, null),
    // fake(),
    { refetchOnWindowFocus: false, enabled: id !== undefined }
  );
}
