import { getEnvFromServer } from "../api/http-common";

export default function getSite(): string | "cpr" {
  return process.env.NEXT_PUBLIC_THEME || "cpr";
}

export async function getSiteAsync() {
  const theme = localStorage.getItem("theme");
  if (theme) return theme;
  const { data } = await getEnvFromServer();
  // Only store the theme if have one set
  if (data?.env?.theme) {
    localStorage.setItem("theme", data?.env?.theme);
  }
  return data;
}
