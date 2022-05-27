import { minYear, currentYear } from '../constants/timedate';
import { PER_PAGE } from '../constants/paging';

export const initialSearchCriteria = {
  query_string: '',
  exact_match: false,
  max_passages_per_doc: 10,
  keyword_filters: {},
  year_range: [minYear, currentYear()],
  sort_field: null,
  sort_order: 'desc',
  limit: PER_PAGE,
  offset: 0,
};
