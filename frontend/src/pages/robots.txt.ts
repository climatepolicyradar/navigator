const crawlableRobotsTxt = `User-agent: *\nAllow: /`;

const uncrawlableRobotsTxt = `User-agent: *\nDisallow: /`;

const isProd = () => {
  return process.env.NEXT_PUBLIC_API_URL && !process.env.NEXT_PUBLIC_API_URL.includes("dev");
};

function Robots() {}

export async function getServerSideProps({ res }) {
  res.setHeader("Content-Type", "text/plan");
  res.write(isProd() ? crawlableRobotsTxt : uncrawlableRobotsTxt);
  res.end();

  return {
    props: {},
  };
}

export default Robots;
