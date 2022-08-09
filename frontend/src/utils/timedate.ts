import { months } from '../constants/timedate';

export const padNumber = (number: number) =>
  number >= 10 ? number : number.toString().padStart(2, '0');

export const convertDate = (data) => {
  const dateObj = new Date(data);
  const year = dateObj.getFullYear();
  const day = padNumber(dateObj.getDate());
  const month = dateObj.getMonth();
  return [year, day, months[month]?.substring(0, 3)];
};
