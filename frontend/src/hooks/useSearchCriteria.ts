import { useQuery, useQueryClient } from 'react-query';
import { initialSearchCriteria } from '../constants/searchCriteria';

export default function useSearchCriteria() {
  const queryClient = useQueryClient();
  return useQuery(
    'searchCriteria',
    () => {
      const existingCriteria = queryClient.getQueryData('searchCriteria');
      return existingCriteria ? existingCriteria : initialSearchCriteria;
    },
    {
      refetchOnWindowFocus: false,
      cacheTime: Infinity,
    }
  );
}
