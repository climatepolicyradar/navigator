import { useTranslation } from 'react-i18next';
import { useAuth } from '@api/auth';
import Layout from '@components/layouts/Main';
import LoaderOverlay from '@components/LoaderOverlay';

function Privacy() {
  const { user } = useAuth();
  const { t } = useTranslation(['common']);
  return (
    <>
      {!user ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Climate Policy Radar | ${t('Privacy')}`}>
          <section>
            <div className="text-content px-4 container mb-12">
              <h1 className="my-8">Privacy notice</h1>
              <h2>Introduction</h2>
              <p>
                Thank you for choosing to be part of our community at Climate
                Policy Radar ("Company," "we", "us", or "our"). As part of our
                core business, we gather confidential information about some of
                our users. We are committed to protecting your personal
                information and your right to privacy. If you have any questions
                or concerns about this privacy notice or our practices with
                regard to your personal information, please contact us at
                info@climatepolicyradar.org.
              </p>
              <p>
                This privacy notice describes how we might use your information
                if you use our app website or use our data products at{' '}
                <a href="https://climatepolicyradar.org/">
                  https://climatepolicyradar.org/
                </a>
              </p>
              <h2>What Information do we collect?</h2>
              <p>
                We collect personal information that you voluntarily provide
                through a number of entryways. These include:
              </p>
              <ul>
                <li>When you register on the Website</li>
                <li>
                  When you express an interest in obtaining information about us
                  or our products and services
                </li>
                <li>When you participate in activities on the Website</li>
                <li>When you contact us</li>
              </ul>
              <p>
                The personal information that we collect depends on the context
                of your interactions with us and the Website, the choices you
                make and the products and features you use.
              </p>
              <p>The types of personal information that we process include:</p>
              <ul>
                <li>Your name</li>
                <li>Postal address</li>
                <li>Email address</li>
                <li>Telephone numbers</li>
                <li>Passwords</li>
                <li>Contact preferences</li>
              </ul>
              <h2>Information automatically collected</h2>
              <p>
                We automatically collect certain information when you visit, use
                or navigate the Website. This information does not reveal your
                specific identity (like your name or contact information) but
                may include device and usage information, such as your IP
                address, browser and device characteristics, operating system,
                language preferences, referring URLs, device name, country,
                location, information about how and when you use our Website and
                other technical information. This information is primarily
                needed to maintain the security and operation of our Website,
                and for our internal analytics and reporting purposes.
              </p>
              <p>
                We also collect information through cookies and similar
                technologies. See our cookie policy{' '}
                <a href="/cookie-policy">here</a>.
              </p>
              <h2>How we use your information</h2>
              <p>
                Climate Policy Radar collects and processes your personal
                information, provided as detailed above, as necessary in order
                to provide you with our service and any related services you may
                request, as well as to:
              </p>
              <ul>
                <li>Facilitate account creation and login process</li>
                <li>
                  Notify you of new or changed services offered in relation to
                  our services
                </li>
                <li>
                  Carry out marketing or training relating to our services
                </li>
                <li>Improve our product offering to you</li>
                <li>To respond to user inquiries/offer support to users</li>
                <li>
                  Comply with laws and regulations in applicable jurisdictions
                </li>
                <li>Post testimonials</li>
              </ul>
              <p>
                By providing us with your personal information, you consent to
                your personal information being collected, held and used in this
                way and for any other use you authorise. Climate Policy Radar
                will only use your personal information for the purposes
                described in this policy or with your express permission.
              </p>
              <h2>Who your information is shared with</h2>
              <p>
                We only share and disclose your information with the following
                categories of third parties. If we have processed your data
                based on your consent and you wish to revoke your consent,
                please contact us using the contact details provided in the
                section below titled "Contact details".
              </p>
              <ul>
                <li>Cloud Computing Services</li>
                <li>Data Analytics Services</li>
                <li>Data Storage Service Providers</li>
                <li>Sales &amp; Marketing Tools</li>
              </ul>
              <p>
                <span className="font-semibold">
                  Your data protection rights:
                </span>{' '}
                Under data protection law, you have rights we need to make you
                aware of. The rights available to you depend on our reason for
                processing your information.
              </p>
              <p>
                <span className="font-semibold">Your right of access:</span> You
                have the right to ask us for copies of your personal
                information.
              </p>
              <p>
                <span className="font-semibold">
                  Right to opt-out of email communications:
                </span>{' '}
                We will send information relating to our service to you by
                email. You can choose to be removed from any mailing list not
                essential to the service by following the instructions in those
                emails to unsubscribe.
              </p>
              <p>
                <span className="font-semibold">
                  Your right to rectification:
                </span>{' '}
                You have the right to ask us to rectify information you think is
                inaccurate. You also have the right to ask us to complete
                information you think is incomplete.
              </p>
              <p>
                <span className="font-semibold"> Your right to erasure:</span>{' '}
                You have the right to ask us to erase your personal information
                in certain circumstances. You can read more about this right
                here.
              </p>
              <p>
                If you hold an account with us, only the owner of the account
                will be able to delete the account. Once an account has been
                closed, any data will be permanently deleted and no longer
                accessible.
              </p>
              <p>
                <span className="font-semibold">
                  Your right to restriction of the processing:
                </span>{' '}
                You have the right to ask us to restrict the processing of your
                information in certain circumstances.
              </p>
              {/* TODO: need to know where to link 'here' to below: */}
              <p>
                <span className="font-bold">
                  Your right to data portability:
                </span>{' '}
                This only applies to the information you have given us. You have
                the right to ask that we transfer the information you gave us
                from one organisation to another, or give it to you. The right
                only applies if we are processing information based on your
                consent or under, or in talks about entering into a contract and
                the processing is automated. You can read more about this right{' '}
                <a href="https://ico.org.uk/your-data-matters/your-right-to-data-portability/">
                  here
                </a>
                .
              </p>
              <h2>Responsibilities</h2>
              <p>
                Everyone that works for Climate Policy Radar is responsible for
                ensuring data is collected, stored and handled appropriately and
                in line with this policy.
              </p>
              <p>
                Our Data Protection Officer is Ingemar Svensson. You can contact
                them by email or via our postal address (see below). Please mark
                the envelope/email ‘For Data Protection Officer’.{' '}
              </p>
              <p>
                If you have questions or comments about this notice, there are
                many ways in which you can contact us, including by email or by
                post.{' '}
              </p>
              <h2>Contact information</h2>
              <p>Our email: info@climatepolicyradar.org</p>
              <p>Our postal address:</p>
              <p>
                Climate Policy Radar CIC <br />
                Sustainable County Hall, 3rd Floor, <br />
                Westminster Bridge Road, <br />
                London, SE1 7PB
              </p>
              <h2>Reviewing and Feedback</h2>
              <p>
                We may update this privacy notice from time to time. The updated
                version will be indicated by an updated "Revised" date and the
                updated version will be effective as soon as it is accessible.
                If we make material changes to this privacy notice, we may
                notify you either by prominently posting a notice of such
                changes or by directly sending you a notification. We encourage
                you to review this privacy notice frequently to be informed of
                how we are protecting your information.
              </p>
            </div>
          </section>
        </Layout>
      )}
    </>
  );
}
export default Privacy;
