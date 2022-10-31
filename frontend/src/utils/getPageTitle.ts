export default function getPageTitle(site: string): string {
  let title = "Climate Policy Radar";
  switch (site) {
    case "cclw":
      title = "Climate Laws of the World";
      break;
  }
  return title;
}
