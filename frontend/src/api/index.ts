import axios from 'axios';
import { storage } from '../utils/storage';
import { ApiClient, AuthClient } from './http-common';

const apiClient = new ApiClient();

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

export const signIn = async (credentials) => {
  return await AuthClient.post(
    'token',
    `grant_type=&username=${credentials.email}&password=${credentials.password}&scope=&client_id=test&client_secret=super_secret`
  ).then(handleApiResponse);
};

export const postFile = async (req: string, data): Promise<any> => {
  return await axios({
    method: 'POST',
    url: `${process.env.NEXT_PUBLIC_API_URL}/${req}`,
    data,
    headers: {
      Authorization: `Bearer ${storage.getToken()}`,
      'Content-Type': 'multipart/form-data',
    },
  }).then((response) => {
    return response.statusText == 'OK'
      ? response.data
      : Promise.reject(Error('Unsuccessful response'));
  });
};

export async function handleApiResponse(response) {
  const data = await response.data;
  console.log(data);
  if (response.statusText === 'OK') {
    console.log('ok??');
    return data;
  } else {
    return Promise.reject(data);
  }
}

export function getUserProfile() {
  return apiClient.get('/users/me', null);
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
