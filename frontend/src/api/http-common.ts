import axios, { AxiosInstance } from "axios";

class ApiClient {
  private baseUrl: string;
  private axiosClient: AxiosInstance;

  constructor(baseUrl = "") {
    if (baseUrl) {
      this.baseUrl = baseUrl;
    } else {
      this.baseUrl = process.env.NEXT_PUBLIC_API_URL;
    }
    this.axiosClient = axios.create();
  }

  /**
   * Submit a GET request and return the response as a mapped promise.
   */
  get(url: string, params?: any) {
    return this.axiosClient
      .get(`${this.baseUrl}${url}`, { params })
      .then((res: any) => res)
      .catch((err: any) => err);
  }
  post(url: string, values: any, config = {}) {
    return this.axiosClient
      .post(`${this.baseUrl}${url}`, values, config)
      .then((res) => res)
      .catch((err) => {
        return Promise.reject(err);
      });
  }
  put(url: string, values: any) {
    return this.axiosClient
      .put(`${this.baseUrl}${url}`, values)
      .then((res) => res)
      .catch((err) => {
        return Promise.reject(err);
      });
  }
}

export { ApiClient };
