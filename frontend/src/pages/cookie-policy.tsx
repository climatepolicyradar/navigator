import { useAuth } from '../api/auth';
import Layout from '../components/layouts/Main';
import LoaderOverlay from '../components/LoaderOverlay';
import './i18n';
import { useTranslation } from 'react-i18next';

const Cookies = () => {
  const { user } = useAuth();
  const { t, i18n, ready } = useTranslation(['common']);
  return (
    <>
      {!user ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Climate Policy Radar | ${t('Cookie policy')}`}>
          <section>
            <div className="text-content px-4 container mb-12">
              <h1 className="my-8">Cookie Policy</h1>
              <p>
                Read about what cookies are, which cookies Climate Policy Radar
                (CPR) use on the Climate Policy Radar Website (CPR Website and
                App), and how can you manage your cookies.
              </p>
              <h2>What are cookies?</h2>
              <p>
                Cookies are small files that are downloaded onto your computer
                when you visit a website. They are used by many websites to make
                them work, or to help them work more efficiently. They also
                provide us with information about how you use the website.
              </p>
              <p>
                Website operators are required by law - specifically the{' '}
                <span className="italic">
                  Privacy and Electronic Communications (EC Directive)
                  (Amendment) Regulations 2011 (UK Regulations)
                </span>{' '}
                - to provide clear and comprehensive information about the use
                of cookies, and ensure that users have consented to this use.
              </p>
              <h2>Which Cookies do we Use?</h2>
              <p>
                Various cookies are in use across the CPR Website and App, with
                the cookies in use subject to changes as the website develops.
                These remain in your browser's subfolder and are activated again
                when you re-visit the website. It helps us to remember your
                information and settings when you visit the website again,
                resulting in a faster online experience for you.
              </p>
              <h3>Google Analytics</h3>
              <p>__ga__gat__</p>
              <p className="italic">
                Used to monitor usage of the CPR Website and App. This
                information allows us to assess how the Website is used.
                Anonymous data about usage (eg number of visitors, visitors'
                country, number of times each page is visited) is collected and
                aggregated to produce website performance reports.
              </p>
              <h2>Log and Usage Data</h2>
              <p>
                Log and usage data is service-related, diagnostic, usage and
                performance information our servers automatically collect when
                you access or use our Website and which we record in log files.
                Depending on how you interact with us, this log data may include
                your IP address, device information, browser type and settings
                and information about your activity on the Website (such as the
                date/time stamps associated with your usage, pages and files
                viewed, searches and other actions you take such as which
                features you use), device event information (such as system
                activity, error reports (sometimes called 'crash dumps') and
                hardware settings).
              </p>
              <h2>Location data</h2>
              <p>
                Location Data. We collect location data such as information
                about your device's location, which can be either precise or
                imprecise. How much information we collect depends on the type
                and settings of the device you use to access the Website. For
                example, we may use GPS and other technologies to collect
                geolocation data that tells us your current location (based on
                your IP address). You can opt-out of allowing us to collect this
                information either by refusing access to the information or by
                disabling your Location setting on your device. However, if you
                choose to opt out, you may not be able to use certain aspects of
                the Services.
              </p>
              <h2>Sharing information via social media platforms</h2>
              <p>
                Our website and apps may have links embedded into pages on
                various social media platforms. Cookies generated by those sites
                are outside of the our control and may change without notice.
                When you share a page or link those sites may set cookies on
                your device or browser and may also make information about you
                publicly available or stored elsewhere. For more information
                about privacy and the cookies used by these services, as well as
                information on how to opt-out, please visit the respective
                social media platforms.
              </p>
              <h2>How can I manage my Cookies?</h2>
              <p>You can use your website browser to:</p>
              <ul>
                <li>Delete all cookies</li>
                <li>Block all cookies</li>
                <li>Allow all cookies</li>
                <li>Block third-party cookies</li>
                <li>Clear all cookies when you close the browser</li>
                <li>
                  Open a 'private browsing' / 'incognito' session (allows you to
                  browse the internet without storing local data)
                </li>
                <li>
                  Install add-ons and plug-ins to extend browser functionality,
                  for example Google have created a{' '}
                  <a href="https://tools.google.com/dlpage/gaoptout">
                    Google Analytics Opt-Out Browser Add-On
                  </a>{' '}
                  for Chrome.
                </li>
              </ul>
              <h2>More information about cookies:</h2>
              <p>
                More information can be found on the Information Commissioner’s
                Office website,{' '}
                <a href="https://ico.org.uk">https://ico.org.uk</a>,{' '}
                <a href="http://aboutcookies.org/">http://aboutcookies.org/</a>{' '}
                and{' '}
                <a href="http://www.allaboutcookies.org/">
                  http://www.allaboutcookies.org/
                </a>
              </p>
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};
export default Cookies;
