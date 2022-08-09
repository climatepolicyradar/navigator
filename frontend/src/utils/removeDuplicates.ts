export const removeDuplicates = (arr, prop) =>
  arr.filter(
    (obj, pos, arr) =>
      arr.map((mapObj) => mapObj[prop]).indexOf(obj[prop]) === pos
  );
