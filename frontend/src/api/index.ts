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
  error?: { error: string };
}

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export const signIn = async (credentials) => {
  return await AuthClient.post(
    '',
    `grant_type=&username=${credentials.email}&password=${credentials.password}&scope=&client_id=test&client_secret=super_secret`
  )
    .then(handleApiSuccess)
    .catch(handleApiError);
};

// may not be using this so not rewriting it for now
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

export async function handleApiSuccess(response) {
  const data = await response.data;
  if (response.statusText === 'OK') {
    return data;
  } else {
    return Promise.reject(data);
  }
}
export async function handleApiError(error) {
  let status = { error: 'There was an error, please try again.' };
  if (error.response.status === 401) {
    status = { error: 'Invalid credentials' };
  }
  return status;
}
export async function handleApiResponse(response) {
  const data = await response.data;
  if (response.statusText === 'OK') {
    return data;
  } else {
    return { error: true };
  }
}

export function getUserProfile() {
  return apiClient.get('/users/me', null);
}

// export async function loginWithEmailAndPassword(data): Promise<AuthResponse> {
//   return window
//     .fetch(`${API_URL}/auth/login`, {
//       method: 'POST',
//       body: JSON.stringify(data),
//     })
//     .then(handleApiResponse);
// }

// Not using this (yet), will need to rewrite

export async function registerWithEmailAndPassword(
  data
): Promise<AuthResponse> {
  return await AuthClient.post(`${API_URL}/activations`, data, {
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/json',
    },
  }).then(handleApiResponse);
}
