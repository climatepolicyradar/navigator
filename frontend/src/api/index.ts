import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  responseType: 'json',
  headers: {
    Authorization:
      'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQG5hdmlnYXRvci5jb20iLCJwZXJtaXNzaW9ucyI6ImFkbWluIiwiZXhwIjoxNjQxOTAxNTExfQ.KvukRuHkpXUGG7JCR3ko6j6lCxelUzn3hIpUg2w6E4M',
    'Content-Type': 'application/json',
  },
});

export const postData = async (req: string, data): Promise<any> => {
  return await api
    .post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`)
    .then((response) => {
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
};

export const getData = async (req: string): Promise<any> => {
  return await api.get(req).then((response) => {
    console.log(response.data);
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};
