import axios, { AxiosInstance, AxiosResponse } from "axios";

export async function getEnvFromServer() {
  return await axios.get("/api/env").then((res: any) => res);
}

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
  get(url: string, params?: any) : Promise<AxiosResponse> {
    // console.log(`GET: ${this.baseUrl}${url}`);
    return this.axiosClient
      .get(`${this.baseUrl}${url}`, { params })
      .then((res: any) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }

  post(url: string, values: any, config = {}) {
    // console.log(`POST: ${this.baseUrl}${url}`);
    return this.axiosClient
      .post(`${this.baseUrl}${url}`, values, config)
      .then((res) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }

  put(url: string, values: any) {
    // console.log(`PUT: ${this.baseUrl}${url}`);
    return this.axiosClient
      .put(`${this.baseUrl}${url}`, values)
      .then((res) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }
}

export { ApiClient };
