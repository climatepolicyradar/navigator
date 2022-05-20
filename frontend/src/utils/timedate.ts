export const convertDate = (data) => {
  const dateObj = new Date(data);
  const year = dateObj.getFullYear();
  const day = dateObj.getDate();
  const month = dateObj.getMonth() + 1;
  return [year, day, month];
};
