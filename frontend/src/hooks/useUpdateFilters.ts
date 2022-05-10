import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useState } from 'react';
import { filterLanguages } from '../helpers';
import useFilters from './useFilters';

export default function useUpdateFilters() {
  const queryClient = useQueryClient();
  const filters = queryClient.getQueryData('filters');
  return useMutation(
    (value) => {
      const x = { value, filters };
      return value;
    },

    {
      onMutate: (value) => {
        const prev = queryClient.getQueryData('filters');

        queryClient.setQueryData(['filters'], (old) => ({
          ...old,
          ...value,
        }));

        return () => queryClient.setQueryData(['filters'], prev);
      },
      onError: (err) => {
        console.log(err);
      },
      onSettled: () => {
        window.scrollTo(0, 0);
      },
    }
  );
}
