import { PER_PAGE } from '../constants/paging';

export const calculatePageCount = (totalItems) => {
  /* Temporary hack because we are only returning a
  max of 100 results  */
  const total = totalItems > 100 ? 100 : totalItems;
  return Math.ceil(total / PER_PAGE);
};
