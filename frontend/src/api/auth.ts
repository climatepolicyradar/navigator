import { initReactQueryAuth } from 'react-query-auth';
import {
  signIn,
  getUserProfile,
  registerWithEmailAndPassword,
  // loginWithEmailAndPassword,
  User,
} from '.';
import { storage } from '../utils/storage';
import Router from 'next/router';
import LoaderOverlay from '../components/LoaderOverlay';

const protectedUrls = ['/add-action', '/account', '/actions', '/search', '/'];

export async function handleUserResponse(data) {
  if (data?.error) {
    return data;
  }
  const { access_token } = data;
  storage.clearToken();
  storage.setToken(access_token);
  //return user;
  return loadUser();
}

async function loadUser() {
  let user = null;
  if (storage.getToken()) {
    try {
      const data = await getUserProfile();
      user = data;
    } catch (error) {
      console.log(error);
    }
  }

  if (user === null && protectedUrls.indexOf(Router.router.pathname) > -1) {
    Router.push('/auth/signin');
  }

  return user;
}

async function loginFn(data) {
  const response = await signIn(data);

  const user = await handleUserResponse(response);
  return user;
}

async function registerFn(data) {
  const response = await registerWithEmailAndPassword(data);
  const user = await handleUserResponse(response);
  return user;
}

async function logoutFn() {
  await storage.clearToken();
  Router.push('/auth/signin');
}

const loaderComponent = () => LoaderOverlay;

const authConfig = {
  loadUser,
  loginFn,
  registerFn,
  logoutFn,
  loaderComponent,
  waitInitial: false,
};

const { AuthProvider, useAuth } = initReactQueryAuth<User>(authConfig);

export { AuthProvider, useAuth };
