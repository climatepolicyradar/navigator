import { useQuery, useQueryClient } from 'react-query';
import { minYear, currentYear } from '../constants/timedate';
import { PER_PAGE } from '../constants/paging';

const initialSearchCriteria = {
  query_string: '',
  exact_match: false,
  max_passages_per_doc: 10,
  keyword_filters: {},
  year_range: [minYear, currentYear()],
  sort_field: 'title',
  sort_order: 'asc',
  limit: PER_PAGE,
  offset: 0,
};

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
