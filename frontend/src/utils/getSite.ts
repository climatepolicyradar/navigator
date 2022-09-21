export default function getSite(): string | "cpr" {
  return process.env.NEXT_PUBLIC_THEME || "cpr";
}
