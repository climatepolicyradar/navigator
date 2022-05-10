import { PER_PAGE } from '../constants/paging';

export const calculatePageCount = (totalItems) => {
  return Math.ceil(totalItems / PER_PAGE);
};
