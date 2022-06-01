import { useQuery, useQueryClient } from 'react-query';

export default function useFilteredCountries(all) {
  const queryClient = useQueryClient();

  return useQuery(
    'filteredCountries',
    () => {
      const existingCountries: any =
        queryClient.getQueryData('filteredCountries');
      return existingCountries?.length ? existingCountries : all;
    },
    {
      refetchOnWindowFocus: false,
      enabled: all.length > 0,
      cacheTime: Infinity,
    }
  );
}
