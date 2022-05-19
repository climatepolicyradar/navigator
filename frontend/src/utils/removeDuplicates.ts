export const removeDuplicates = (arr, prop) => {
  return arr.filter((obj, pos, arr) => {
    return arr.map((mapObj) => mapObj[prop]).indexOf(obj[prop]) === pos;
  });
};
