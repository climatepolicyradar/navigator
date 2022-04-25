import { useQuery } from 'react-query';

const initialSearchCriteria = {
  query_string: '',
  exact_match: false,
  max_passages_per_doc: 10,
  keyword_filters: {},
  year_range: [1900, 2022],
  sort_field: 'title',
  sort_order: 'desc',
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
