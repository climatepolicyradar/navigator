import axios from 'axios';

let token;

const authapi = axios.create({
  baseURL: 'http://localhost:8000/api/',
  responseType: 'json',
  headers: {
    accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export const getAuth = async () => {
  await authapi
    .post(
      'token',
      'grant_type=&username=user%40navigator.com&password=password&scope=&client_id=test&client_secret=super_secret'
    )
    .then((response) => {
      token = response.data.access_token;
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
};

export const postFile = async (req: string, data): Promise<any> => {
  // return await fileapi.post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`, data)
  return await axios({
    method: 'POST',
    url: `${process.env.NEXT_PUBLIC_API_URL}/${req}`,
    data,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data',
    },
  }).then((response) => {
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};
export const postData = async (req: string, data): Promise<any> => {
  // return await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${req}`, data)
  return await axios({
    method: 'POST',
    url: `${process.env.NEXT_PUBLIC_API_URL}/${req}`,
    data,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  }).then((response) => {
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};

export const getData = async (req: string): Promise<any> => {
  return await axios({
    method: 'GET',
    url: `${process.env.NEXT_PUBLIC_API_URL}/${req}`,
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  }).then((response) => {
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};
