import axios from 'axios';
import { storage } from '../utils/storage';
import { ApiClient, AuthClient } from './http-common';

const apiClient = new ApiClient();

interface AuthResponse {
  jwt: string;
}
interface ResetResponse {
  value: boolean;
}

export interface User {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  error?: { error: string };
  activated?: boolean;
}

export const signIn = async (credentials) => {
  return await AuthClient.post(
    '',
    `username=${credentials.email}&password=${credentials.password}`
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
  const data = await response;
  if (response.status === 200) {
    return data;
  } else {
    return Promise.reject(data);
  }
}
export async function handleApiError(error) {
  const message = error?.response?.data.detail
    ? error?.response?.data.detail
    : 'There was an error, please try again later.';
  return { error: message };
}

export async function getUserProfile() {
  return await apiClient.get('/users/me', null);
}

export async function registerWithEmailAndPassword(
  data
): Promise<AuthResponse> {
  return await apiClient
    .post(`/activations`, data)
    .then(handleApiSuccess)
    .catch(handleApiError);
}

export async function handleResetRequest(data: string): Promise<ResetResponse> {
  return await apiClient
    .post(`/password-reset/${data}`, null)
    .then(handleApiSuccess)
    .catch(handleApiError);
}
