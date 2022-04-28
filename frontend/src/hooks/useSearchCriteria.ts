import { useQuery } from 'react-query';
import { minYear, currentYear } from '../constants/timedate';

const initialSearchCriteria = {
  query_string: '',
  exact_match: false,
  max_passages_per_doc: 10,
  keyword_filters: {},
  year_range: [minYear, currentYear()],
  sort_field: 'title',
  sort_order: 'asc',
  limit: 10,
  offset: 0,
};

export default function useSearchCriteria() {
  return useQuery(
    'searchCriteria',
    () => {
      return initialSearchCriteria;
    },
    { refetchOnWindowFocus: false }
  );
}
