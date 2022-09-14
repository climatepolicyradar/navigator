import { initReactQueryAuth } from "react-query-auth";
import Router from "next/router";
import { signIn, getUserProfile, registerWithEmailAndPassword, User, handleResetRequest } from ".";
import { storage } from "../utils/storage";
import LoaderOverlay from "@components/LoaderOverlay";

const unprotectedUrls = ["/auth/sign-in", "/auth/sign-up", "/auth/activate-account", "/auth/reset-password", "/auth/reset-request"];
const protectedUrls = ["/account"];

export async function handleUserResponse(response) {
  const res = await response;
  if (res.error) return res;

  // user has logged in
  if (res.data?.access_token) {
    const { access_token } = res.data;
    storage.clearToken();
    storage.setToken(access_token);
    return loadUser();
  }
  // user has activated
  return { activated: true };
}

async function loadUser() {
  let user = null;
  try {
    const response = await getUserProfile();
    user = response.data;
  } catch (error) {
    console.log(error);
  }

  if (user === null && protectedUrls.indexOf(Router.router.pathname) !== -1) {
    Router.push("/auth/sign-in");
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
  storage.clearToken();
  return Router.push("/");
}

const loaderComponent = () => LoaderOverlay;

const resetRequest = async (data: string) => {
  const response = await handleResetRequest(data);
  return response;
};

const authConfig = {
  loadUser,
  loginFn,
  registerFn,
  logoutFn,
  loaderComponent,
  waitInitial: false,
};

const { AuthProvider, useAuth } = initReactQueryAuth<User>(authConfig);

export { AuthProvider, useAuth, resetRequest };
