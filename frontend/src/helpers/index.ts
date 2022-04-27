export const fakePromise = (delay, value) => {
  return new Promise(function (resolve) {
    setTimeout(resolve, delay, value); // Note the order, `delay` before `value`
  });
};
export const filterLanguages = (langs) => {
  return langs.filter((lang) => lang.part1_code !== null);
};
