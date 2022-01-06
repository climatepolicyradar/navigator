import axios from 'axios';

export const postData = async (req: string, data): Promise<any> => {
  return await axios
    .post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`)
    .then((response) => {
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
};
