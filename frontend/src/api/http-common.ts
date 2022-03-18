import axios from 'axios';
import { storage } from '../utils/storage';

export default class ApiClient {
  private baseUrl;
  private axiosClient;

  constructor(baseUrl = '') {
    if (baseUrl) {
      this.baseUrl = baseUrl;
    } else {
      this.baseUrl = process.env.NEXT_PUBLIC_API_URL;
    }
    this.axiosClient = axios.create({ withCredentials: true });
    this.axiosClient.interceptors.request.use(
      (config) => {
        const token = storage.getToken();
        if (token) {
          // eslint-disable-next-line no-param-reassign
          config.headers.common.Authorization = `Bearer ${token}`;
        }
        return config;
      },
    );
  }

  /**
   * Submit a GET request and return the response as a mapped promise.
   */
  get(url, params) {
    return this.axiosClient.get(`${this.baseUrl}${url}`, { params })
      .then((res) => res.data)
      .catch((err) => Promise.reject(err));
  }
  post(url, values ) {
    return this.axiosClient.post(`${this.baseUrl}${url}`, values )
      .then((res) => res.data)
      .catch((err) => {
        console.log(err)
        return Promise.reject(err)});
  }
}
