import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  responseType: 'json',
  headers: {
    Authorization:
      'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQG5hdmlnYXRvci5jb20iLCJwZXJtaXNzaW9ucyI6ImFkbWluIiwiZXhwIjoxNjQxOTM3ODU4fQ.w29_aKrXf_tKGblAx30MYr1Pwu1wMWfIpPTjov2xCOc',
    'Content-Type': 'application/json',
  },
});
const authapi = axios.create({
  baseURL: 'http://localhost:8000/api/',
  responseType: 'json',
  headers: {
    accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});
const fileapi = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  responseType: 'json',
  headers: {
    Authorization:
      'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQG5hdmlnYXRvci5jb20iLCJwZXJtaXNzaW9ucyI6ImFkbWluIiwiZXhwIjoxNjQxOTM3ODU4fQ.w29_aKrXf_tKGblAx30MYr1Pwu1wMWfIpPTjov2xCOc',
    'Content-Type': 'multipart/form-data',
  },
});

const getAuth = async (req) => {
  await authapi
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

export const postFile = async (req: string, data): Promise<any> => {
  console.log(data);
  return await fileapi
    .post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`, data)
    .then((response) => {
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
};
export const postData = async (req: string, data): Promise<any> => {
  console.log(data);
  return await api
    .post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`, data)
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
