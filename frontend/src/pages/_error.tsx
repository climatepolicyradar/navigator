import { ExternalLink } from "@components/ExternalLink";
import Layout from "../components/layouts/Main";

function Error({ statusCode }) {
  return (
    <Layout title={statusCode}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">{statusCode === 404 ? "Sorry, we can't find that page" : "Sorry, an error has occurred loading this page"}</h1>
          <p>
            Please <ExternalLink url="mailto:support@climatepolicyradar.org">contact us</ExternalLink> if you would like to report the issue.
          </p>
        </div>
      </section>
    </Layout>
  );
}

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;
