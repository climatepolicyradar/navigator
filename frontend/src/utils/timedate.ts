import { months } from '../constants/timedate';

export const convertDate = (data) => {
  const dateObj = new Date(data);
  const year = dateObj.getFullYear();
  const day = padNumber(dateObj.getDate());
  const month = dateObj.getMonth();
  return [year, day, months[month]?.substring(0, 3)];
};
export const padNumber = (number) => {
  return number >= 10 ? number : number.toString().padStart(2, '0');
};
