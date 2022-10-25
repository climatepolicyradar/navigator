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
          <p>
            The database also features climate litigation cases from over 40 countries. These cases raise issues of law or fact regarding the science of climate change and/or
            climate change mitigation and adaptation policies or efforts before an administrative, judicial or other investigatory body. The database uses summaries from the Sabin
            Center's <ExternalLink url="http://climatecasechart.com/non-us-climate-change-litigation/">Climate Case Chart</ExternalLink>. Work to identify new cases is also
            supported by a{" "}
            <ExternalLink url="https://climate.law.columbia.edu/content/global-network-peer-reviewers-climate-litigation">Global Network of Peer Reviewers</ExternalLink>,
            coordinated by the Sabin Center. This dataset does not include the United States - to access information about climate change litigation in the US, please{" "}
            <ExternalLink url="http://climatecasechart.com/us-climate-change-litigation/">
              click here to go to the Sabin Center / Arnold & Porter Kaye Scholer database
            </ExternalLink>
            . This will take you to a different website and will open in a new window.
          </p>
          <h2>Use and reference of the data</h2>
          <p>
            The Grantham Research Institute encourages the use of this database. Users are welcome to download, save, or distribute the results electronically or in any other
            format, without written permission of the authors.
          </p>
          <p>
            <span className="block font-bold italic">Please reference the source as follows:</span>
            Climate Change Laws of the World database, Grantham Research Institute on Climate Change and the Environment and Sabin Center for Climate Change Law. Available at{" "}
            <ExternalLink url="https://climate-laws.org">climate-laws.org</ExternalLink>.
          </p>
          <h2>Invitation to contribute</h2>
          <p>
            We aim for the datasets to be as comprehensive and accurate as possible. However, there is no claim to have identified every relevant law, policy or court case in the
            countries covered. We invite anyone to draw our attention to any information we may have missed or any errors or updates to existing data. Please follow{" "}
            <ExternalLink url="https://docs.google.com/forms/d/e/1FAIpQLSdBdX2mLzFdeP8sTd_K7dsv8oylX6EBQucR_HhiXYZm1GA6gg/viewform">this link</ExternalLink> or email{" "}
            <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink> to contribute.
          </p>
        </div>
      </section>
    </Layout>
  );
};

export default About;
