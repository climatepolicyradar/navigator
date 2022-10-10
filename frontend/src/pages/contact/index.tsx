import Layout from "@components/layouts/Main";
import { ExternalLink } from "@components/ExternalLink";

const Contact = () => {
  return (
    <Layout title={`Climate Policy Radar | Contact`}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Contact</h1>
          <p>
            Please get in touch with the Climate Change Laws of the World team with any questions or comments by emailing{" "}
            <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink>
          </p>
          <p>
            We particularly welcome comments and inputs about the content of the database, including laws and policies we may have missed. We are a small team, and rely on the
            collaboration of our global stakeholders to support our efforts to keep the database up to date.
          </p>
          <h2>Correspondence address, telephone number and email</h2>
          <p>As many of our staff regularly work remotely, the best way to contact us is by email.</p>
          <div className="md:grid grid-cols-2 mb-6">
            <address>
              LSE Houghton Street
              <br />
              London
              <br />
              WC2A 2AE
              <br />
              UK
            </address>
            <div>
              <p><ExternalLink url="tel:+44 (0)20 7107 5865">+44 (0)20 7107 5865</ExternalLink></p>
              <p>Email for general enquiries: <ExternalLink url="mailto:Gri@lse.ac.uk">Gri@lse.ac.uk</ExternalLink></p>
            </div>
          </div>
          <h2>Media enquiries</h2>
          <p>
            <ExternalLink url="tel:+44 (0)20 7107 5442">+44 (0)20 7107 5442</ExternalLink>
          </p>
          <p>
            Email: <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink>
          </p>
          <h2>Finding specific contact information</h2>
          <p>
            For details of individual staff members working at the Grantham Research Institute check our{" "}
            <ExternalLink url="https://www.lse.ac.uk/granthaminstitute/people/institute-staff/">staff directory.</ExternalLink>
          </p>
        </div>
      </section>
    </Layout>
  );
};

export default Contact;

// Contact [title]
// Please get in touch with the Climate Change Laws of the World team with any questions or comments by emailing gri.cgl@lse.ac.uk.

// We particularly welcome comments and inputs about the content of the database, including laws and policies we may have missed. We are a small team, and rely on the collaboration of our global stakeholders to support our efforts to keep the database up to date.

// Correspondence address, telephone number and email [sub-title]

// As many of our staff regularly work remotely, the best way to contact us is by email.
// [Column 1]
// LSE
// Houghton Street
// London
// WC2A 2AE
// UK
// [column 2]
// +44 (0)20 7107 5865
// Email for general enquiries: Gri@lse.ac.uk
// Media enquiries [Sub-title]
// +44 (0)20 7107 5442
// Email: gri.media@lse.ac.uk
// Finding specific contact information [sub-title]
// For details of individual staff members working at the Grantham Research Institute check our staff directory (url: https://www.lse.ac.uk/granthaminstitute/people/institute-staff/)
