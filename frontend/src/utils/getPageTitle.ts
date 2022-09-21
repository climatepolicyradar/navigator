import getSite from "./getSite";

export default function getPageTitle(): string {
  const site = getSite();
  let title = "Climate Policy Radar";
  switch (site) {
    case "cclw":
      title = "Climate Laws of the World";
      break;
  }
  return title;
}
