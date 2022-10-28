import { getEnvFromServer } from "../api/http-common";

export default function getSite(): string | "cpr" {
  return process.env.NEXT_PUBLIC_THEME || "cpr";
}

export async function getSiteAsync() {
  const theme = localStorage.getItem("theme");
  if (theme) return theme;
  const { data } = await getEnvFromServer();
  const themeResponse = data?.env?.theme;
  // Only store the theme if have one set
  if (themeResponse) {
    localStorage.setItem("theme", themeResponse);
  }
  // Will return null if not found
  return themeResponse;
}
