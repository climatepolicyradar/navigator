import axios from 'axios';
import { storage } from '../utils/storage';

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
      // window.localStorage.setItem('jwt', response.data.access_token);
      storage.clearToken();
      storage.setToken(response.data.access_token);
      // console.log(response);
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
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
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
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
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
      Authorization: `Bearer ${window.localStorage.getItem('jwt')}`,
      'Content-Type': 'application/json',
    },
  }).then((response) => {
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};

/* NEW AUTH */

interface AuthResponse {
  jwt: string;
}

export interface User {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_superuser: boolean;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function handleApiResponse(response) {
  const data = await response.json();

  if (response.ok) {
    return data;
  } else {
    return Promise.reject(data);
  }
}

export async function getUserProfile() {
  console.log('get user profile');
  // console.log(storage.getToken());
  return await fetch(`${API_URL}/users/me`, {
    headers: {
      Authorization: `Bearer ${storage.getToken()}`,
    },
  }).then(handleApiResponse);
}

export async function loginWithEmailAndPassword(data): Promise<AuthResponse> {
  return window
    .fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    .then(handleApiResponse);
}

export async function registerWithEmailAndPassword(
  data
): Promise<AuthResponse> {
  return window
    .fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
    .then(handleApiResponse);
}
