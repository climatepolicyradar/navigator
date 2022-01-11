import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  responseType: 'json',
  headers: {
    Authorization:
      'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQG5hdmlnYXRvci5jb20iLCJwZXJtaXNzaW9ucyI6ImFkbWluIiwiZXhwIjoxNjQxOTM3ODU4fQ.w29_aKrXf_tKGblAx30MYr1Pwu1wMWfIpPTjov2xCOc',
    'Content-Type': 'application/json',
  },
});
export const auth = axios.create({
  baseURL: 'http://localhost:8000/api/',
  responseType: 'json',
  headers: {
    accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

const getAuth = async (req) => {
  await auth
    .post(
      'token',
      'grant_type=&username=user%40navigator.com&password=password&scope=&client_id=test&client_secret=super_secret'
    )
    .then((response) => {
      console.log(response);
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
};

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
    // console.log(response.data);
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};
