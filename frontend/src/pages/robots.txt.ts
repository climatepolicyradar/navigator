const crawlableRobotsTxt = `User-agent: *\nAllow: /`;

const uncrawlableRobotsTxt = `User-agent: *\nDisallow: /`;

function Robots() { }

export async function getServerSideProps({ res }) {
  res.setHeader("Content-Type", "text/plan");
  res.write(process.env.ROBOTS === "true" ? crawlableRobotsTxt : uncrawlableRobotsTxt);
  res.end();

  console.log(process.env.ROBOTS);

  return {
    props: {},
  };
}

export default Robots;
