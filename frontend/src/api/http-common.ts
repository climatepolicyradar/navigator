import axios, { AxiosInstance, AxiosResponse } from "axios";

export async function getEnvFromServer() {
  const result: AxiosResponse = await axios.get("/api/env").then((res: any) => res);
  console.log(`getEnvFromServer ${result.data?.env?.api_url}`);
  return result
}

class ApiClient {
  private baseUrl: string;
  private axiosClient: AxiosInstance;

  constructor(baseUrl = "") {
    console.log(`ApiClient is using ${baseUrl}`);
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
    console.log(`GET: ${this.baseUrl}${url}`);
    return this.axiosClient
      .get(`${this.baseUrl}${url}`, { params })
      .then((res: any) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }

  post(url: string, values: any, config = {}) {
    console.log(`POST: ${this.baseUrl}${url}`);
    return this.axiosClient
      .post(`${this.baseUrl}${url}`, values, config)
      .then((res) => res)
      .catch((err) => {
        console.log(err);
        return Promise.reject(err);
      });
  }

  put(url: string, values: any) {
    console.log(`PUT: ${this.baseUrl}${url}`);
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
