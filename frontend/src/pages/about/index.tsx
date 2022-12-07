import Link from "next/link";
import Layout from "@components/layouts/Main";
import { ExternalLink } from "@components/ExternalLink";

const About = () => {
  return (
    <Layout title={`About`}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">About</h1>
          <p>
            The Climate Change Laws of the World database builds on more than a decade of data collection by the Grantham Research Institute at LSE and the Sabin Center at Columbia
            Law School. The database is powered by machine learning and natural language processing technology developed by Climate Policy Radar.
          </p>
          <p>
            Climate Change Laws of the World covers national-level climate change legislation and policies globally. The database covers climate and climate-related laws, as well
            as laws and policies promoting low carbon transitions, which reflects the relevance of climate policy in areas including energy, transport, land use, and climate
            resilience. This database originates from a collaboration between the Grantham Research Institute and GLOBE International on a series of Climate Legislation Studies.
          </p>
          <h2>Use and reference of the data</h2>
          <p>
            For information about using and referencing the data, please see our{" "}
            <Link href="/terms-of-use">
              Terms of Use
            </Link>
            .
          </p>
          <h2>Invitation to contribute</h2>
          <p>
            We aim for the datasets to be as comprehensive and accurate as possible. However, there is no claim to have identified every relevant law, policy or court case in the
            countries covered. We invite anyone to draw our attention to any information we may have missed or any errors or updates to existing data. Please{" "}
            <ExternalLink url="https://docs.google.com/forms/d/e/1FAIpQLScNy6pZTInQKdxNDaZPKyPGgbfRktstzgVDjGBCeTnLVzl3Pg/viewform">fill out our form</ExternalLink> or email{" "}
            <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink> to contribute.
          </p>
        </div>
      </section>
    </Layout>
  );
};

export default About;
