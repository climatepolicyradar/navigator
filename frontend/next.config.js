// application level redirects, old endpoints no longer supported
const defaultRedirects = [
  {
      source: "/auth/:id*",
      destination: "/",
      permanent: true,
    },
    {
      source: "/account",
      destination: "/",
      permanent: true,
    },
    {
      source: "/users/:id*",
      destination: "/",
      permanent: true,
    },
    {
      source: "/litigation/:id*",
      destination: "/",
      permanent: false, // will become a page eventually
    },
  ];
 
// for pages that are not in cclw's sitemap
const cclwRedirects = [
    { source: "/cookie-policy", destination: "/", permanent: true },
    { source: "/privacy", destination: "/", permanent: true },
];

// for pages that are not in cpr's sitemap
const cprRedirects = [
    { source: "/about", destination: "/", permanent: true },
    { source: "/acknowledgements", destination: "/", permanent: true },
    { source: "/contact", destination: "/", permanent: true },
    { source: "/methodology", destination: "/", permanent: true },
];

// function that will return default, theme and file based redirects
function get_redirects() {
    const REDIRECT_FILE = process.env.NEXT_REDIRECT_FILE || "default.json";
    console.log(`Getting redirects from file: ${REDIRECT_FILE}`);
    const redirectsFromFile = require(`./redirects/${REDIRECT_FILE}`);
    let themeRedirects = [];
    if (process.env.THEME === "cclw") {
      console.log("THEME is cclw");
      themeRedirects = cclwRedirects; 
    }
    if (process.env.THEME === "cpr") {
      console.log("THEME is cpr");
      themeRedirects = cprRedirects;
    }

    console.log(`Also applying theme redirects for ${process.env.THEME}`);

    return defaultRedirects
      .concat(themeRedirects)
      .concat(redirectsFromFile);
}

module.exports = (phase) => {
  console.log("Starting at phase:", phase);

  const nextConfig = {
    i18n: {
      locales: ["en", "fr"],
      defaultLocale: "en",
    },
    pageExtensions: ["tsx", "ts"],
  };

  nextConfig.redirects = async() => {
    console.log("-X-X-X-X-");
    const reds = get_redirects();
    console.log(JSON.stringify(reds, null, 4));
    return reds;
  };
  return nextConfig;
};
