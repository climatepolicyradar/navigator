export const storage = {
  getToken: () => JSON.parse(localStorage.getItem('jwt')),
  setToken: (token) => localStorage.setItem('jwt', JSON.stringify(token)),
  clearToken: () => localStorage.removeItem('jwt'),
};
