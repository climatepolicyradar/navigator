export const sortData = (data, prop) => {
  const myData = data.sort((a, b) => {
    if (a[prop] < b[prop]) {
      return -1;
    }
    if (a[prop] > b[prop]) {
      return 1;
    }
    return 0;
  });

  return myData;
};
