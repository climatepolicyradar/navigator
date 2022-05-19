import axios from 'axios';
import { storage } from '../utils/storage';

class ApiClient {
  private baseUrl;
  private axiosClient;

  constructor(baseUrl = '') {
    if (baseUrl) {
      this.baseUrl = baseUrl;
    } else {
      this.baseUrl = process.env.NEXT_PUBLIC_API_URL;
    }
    this.axiosClient = axios.create({ withCredentials: true });
    this.axiosClient.interceptors.request.use((config) => {
      const token = storage.getToken();
      if (token) {
        // eslint-disable-next-line no-param-reassign
        config.headers.common.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  /**
   * Submit a GET request and return the response as a mapped promise.
   */
  get(url, params) {
    return this.axiosClient
      .get(`${this.baseUrl}${url}`, { params })
      .then((res) => res)
      .catch((err) => Promise.reject(err));
  }
  post(url, values, config = {}) {
    // console.log('values: ');
    // console.log(values);
    return this.axiosClient
      .post(`${this.baseUrl}${url}`, values, config)
      .then((res) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }
  put(url, values) {
    return this.axiosClient
      .put(`${this.baseUrl}${url}`, values)
      .then((res) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }
}

const AuthClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_LOGIN_API_URL,
  responseType: 'json',
  headers: {
    accept: 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

export { ApiClient, AuthClient };
