import { useMutation, useQueryClient } from 'react-query';
import useSearchCriteria from './useSearchCriteria';
import { multipleValuesAllowed } from '../constants/filters';

export default function useUpdateSearchFilters() {
  const queryClient = useQueryClient();
  const { data } = useSearchCriteria();

  const getKeyAndValue = (obj) => {
    const key = Object.keys(obj)[0];
    const val = Object.values(obj)[0];
    return [key, val];
  };

  const processFilter = (value) => {
    const prev = queryClient.getQueryData('searchCriteria');
    const { keyword_filters } = prev;
    let [key, val] = getKeyAndValue(value);
    // check if filter allows multiple values and there is a value already for that key
    // if true, add to that array, otherwise just make the value an array with a single value
    if (multipleValuesAllowed.indexOf(key) > -1 && keyword_filters[key]) {
      val = [...keyword_filters[key], val];
    } else {
      val = [val];
    }
    return {
      ...data,
      keyword_filters: { ...keyword_filters, [key]: val },
    };
  };

  return useMutation(
    (value) => {
      const newObj = processFilter(value);
      return queryClient.setQueryData('searchCriteria', (old) => {
        return {
          ...old,
          ...newObj,
        };
      });
    },

    {
      onError: (err) => {
        console.log(err);
      },
    }
  );
}
