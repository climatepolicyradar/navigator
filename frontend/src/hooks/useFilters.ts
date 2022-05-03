import { useQuery, useMutation } from 'react-query';
import { useState } from 'react';

export default function useFilters() {
  return useQuery('filters', () => {
    return {};
  });
}
