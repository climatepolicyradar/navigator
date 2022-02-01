export const months = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

export const yearRange = () => {
  const min = 1947;
  const max = new Date().getFullYear();
  const arr = [];
  for (let i = min; i <= max; i++) {
    arr.push(i);
  }
  return arr.sort(function (a, b) {
    return b - a;
  });
};

export const daysInMonth = (month, year) => {
  // Use 1 for January, 2 for February, etc.
  return new Date(year, month, 0).getDate();
};

export const dayRange = (month) => {};
