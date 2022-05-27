export const fakePromise = (delay, value) => {
  return new Promise(function (resolve) {
    setTimeout(resolve, delay, value); // Note the order, `delay` before `value`
  });
};
export const filterLanguages = (langs) => {
  return langs.filter((lang) => lang.part1_code !== null);
};
export const truncateString = (str: string, num: number): string => {
  if (str.length <= num) {
    return str;
  }
  return str.slice(0, num) + '...';
};
