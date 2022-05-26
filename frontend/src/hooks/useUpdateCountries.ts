import { useMutation, useQueryClient } from 'react-query';
import useNestedLookups from './useNestedLookups';

export default function useUpdateCountries() {
  const queryClient = useQueryClient();

  return useMutation(
    (value?: any) => {
      console.log(value);
      const { regionName, regions, countries } = value;
      const region = regions.find((item) => item.display_value === regionName);
      let newList = countries;
      if (region) {
        newList = countries.filter((item: any) => item.parent_id === region.id);
      }

      return queryClient.setQueryData('filteredCountries', newList);
    },

    {
      onError: (err) => {
        console.log(err);
      },
    }
  );
}
