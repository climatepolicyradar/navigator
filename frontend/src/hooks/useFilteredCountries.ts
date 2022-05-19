import { useQuery, useQueryClient } from 'react-query';

export default function useFilteredCountries(all) {
  const queryClient = useQueryClient();

  return useQuery(
    'filteredCountries',
    () => {
      const existingCountries = queryClient.getQueryData('filteredCountries');

      return existingCountries ? existingCountries : all;
    },
    {
      refetchOnWindowFocus: false,
      enabled: all.length > 0,
    }
  );
}
