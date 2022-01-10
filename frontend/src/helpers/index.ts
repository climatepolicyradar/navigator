export const fakePromise = (delay, value) => {
  return new Promise(function (resolve) {
    setTimeout(resolve, delay, value); // Note the order, `delay` before `value`
  });
};
