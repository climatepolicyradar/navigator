import { useQuery, useQueryClient } from 'react-query';
import { minYear, currentYear } from '../constants/timedate';
import { PER_PAGE } from '../constants/paging';
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
    }
  );
}
