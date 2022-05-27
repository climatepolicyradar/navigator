import { useMutation, useQueryClient } from 'react-query';
import useSearchCriteria from './useSearchCriteria';
import { multipleValuesAllowed } from '../constants/filters';

export default function useUpdateSearchFilters() {
  const queryClient = useQueryClient();
  const { data }: any = useSearchCriteria();

  const getKeyAndValue = (obj: any): any[] => {
    // get first key and value
    const key = Object.keys(obj)[0];
    const val = Object.values(obj)[0];
    return [key, val];
  };

  const removeProperty = (key: string, keyword_filters) => {
    const { [key]: remove, ...rest } = keyword_filters;
    return rest;
  };

  const actions = {
    delete: (key, val, keyword_filters) => {
      let valArray = [val];
      let new_keyword_filters = {};
      if (multipleValuesAllowed.indexOf(key) > -1) {
        // remove value from array
        valArray = keyword_filters[key].filter((item) => {
          return item !== val;
        });
        if (!valArray.length) {
          // if array becomes empty then remove the property from the keyword_filters object
          new_keyword_filters = removeProperty(key, keyword_filters);
        } else {
          // if array still is not empty, assign new filtered array to key
          new_keyword_filters = { ...keyword_filters, [key]: valArray };
        }
      } else {
        // not multiple values, so just remove the property from the keyword_filters object
        new_keyword_filters = removeProperty(key, keyword_filters);
      }
      return new_keyword_filters;
    },
    update: (key, val, keyword_filters) => {
      let valArray = [val];
      if (multipleValuesAllowed.indexOf(key) > -1 && keyword_filters[key]) {
        valArray = [...keyword_filters[key], val];
      }
      return { ...keyword_filters, [key]: valArray };
    },
  };

  const processFilter = (value: any) => {
    const prev: any = queryClient.getQueryData('searchCriteria');
    const { keyword_filters } = prev;
    let [key, val] = getKeyAndValue(value);
    const { action } = val.length ? value : { action: 'delete' };
    const new_keyword_filters = actions[action](key, val, keyword_filters);

    return {
      ...data,
      keyword_filters: new_keyword_filters,
    };
  };

  return useMutation(
    (value: any) => {
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
