export const storage = {
  getToken: () => JSON.parse(window.localStorage.getItem('jwt')),
  setToken: (token) =>
    window.localStorage.setItem('jwt', JSON.stringify(token)),
  clearToken: () => window.localStorage.removeItem('jwt'),
};
