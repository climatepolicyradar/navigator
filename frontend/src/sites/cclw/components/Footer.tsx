/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/Logo";
import { date } from "yup";

type TFooterItem = {
  title: string;
  links: TLinkItem[];
};

type TLinkItem = {
  text: string;
  url: string;
  external: boolean;
};

const navLinks: TFooterItem = {
  // {
  //   title: "Navigation",
  //   links: [
  //     {
  //       text: "About",
  //       url: "/about",
  //       external: false,
  //     },
  //     {
  //       text: "Methodology",
  //       url: "/methodology",
  //       external: false,
  //     },
  //     {
  //       text: "Acknowledgements",
  //       url: "/acknowledgements",
  //       external: false,
  //     },
  //     {
  //       text: "Terms of use",
  //       url: "/terms-of-use",
  //       external: false,
  //     },
  //     {
  //       text: "Privacy and data protection",
  //       url: "https://www.lse.ac.uk/lse-information/privacy-policy",
  //       external: true,
  //     },
  //   ],
  // },
  // {
  title: "Grantham Research Institute",
  links: [
    {
      text: "Grantham Research Institute",
      url: "https://www.lse.ac.uk/granthaminstitute/",
      external: true,
    },
    {
      text: "Research areas",
      url: "https://www.lse.ac.uk/granthaminstitute/research-areas/",
      external: true,
    },
    {
      text: "Publications",
      url: "https://www.lse.ac.uk/granthaminstitute/publications/",
      external: true,
    },
    {
      text: "Events",
      url: "https://www.lse.ac.uk/granthaminstitute/events/",
      external: true,
    },
    {
      text: "News and commentaries",
      url: "https://www.lse.ac.uk/granthaminstitute/news-and-commentary/",
      external: true,
    },
    {
      text: "Sign up to Grantham Research Institute's newsletter",
      url: "https://www.lse.ac.uk/granthaminstitute/mailing-list/ ",
      external: true,
    },
  ],
  // },
};

const Footer = () => {
  const renderLink = (item: TLinkItem) => {
    if (item.external) {
      return <ExternalLink url={item.url}>{item.text}</ExternalLink>;
    }
    return (
      <Link href={item.url}>
        <a>{item.text}</a>
      </Link>
    );
  };

  return (
    <footer className="flex flex-col bg-grey-400 mt-12">
      <div className="py-12">
        <div className="container">
          <p className="font-bold text-xl mb-8">Climate Change Laws of the World</p>
          {/* <p className="mb-10">In partnership with the Sabin Center for Climate Change Law, Columbia Law School</p> */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div key={navLinks.title} className="footer__section">
              <h5 className="font-normal">{navLinks.title}</h5>
              <div className="grid gap-y-5 md:grid-cols-2">
                <ul>
                  {navLinks.links.map((link) => (
                    <li key={link.text} className="mb-1">
                      {renderLink(link)}
                    </li>
                  ))}
                </ul>
                <div>
                  <div className="mb-6 footer__section flex gap-6">
                    <div>Contact</div>
                    <div>
                      <ExternalLink url="mailto:gri.cgl@lse.co.uk" className="block">
                        gri.cgl@lse.co.uk
                      </ExternalLink>
                      <Link href="/contact">
                        <a>Full contact details</a>
                      </Link>
                    </div>
                  </div>
                  <div className="footer__section">
                    <div>Follow Grantham Research Institute</div>
                    <div className="flex items-start gap-6 footer__social-links">
                      <ExternalLink url="https://twitter.com/GRI_LSE">
                        <img src="/images/social/twitter.svg" alt="Twitter Logo" />
                      </ExternalLink>
                      <ExternalLink url="https://www.youtube.com/user/GranthamResearch">
                        <img src="/images/social/youtube.svg" alt="YouTube Logo" />
                      </ExternalLink>
                      <ExternalLink url="https://www.linkedin.com/company/grantham-research-institute-lse/">
                        <img src="/images/social/linkedIn.svg" alt="LinkedIn Logo" />
                      </ExternalLink>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="footer__section md:w-1/2 lg:mx-auto">
              <h5 className="font-normal">Climate Policy Radar</h5>
              <p>Using AI and data science to map the world's climate policies</p>
              <ul className="mb-6">
                <li className="mb-1">
                  <ExternalLink url="https://www.climatepolicyradar.org">www.climatepolicyradar.org</ExternalLink>
                </li>
                {process.env.NEXT_PUBLIC_CPR_NEWSLETTER_URL && (
                  <li className="mb-1">
                    <ExternalLink url={process.env.NEXT_PUBLIC_CPR_NEWSLETTER_URL}>Sign up to Climate Policy Radar's newsletter</ExternalLink>
                  </li>
                )}
                <li className="mb-1">
                  <ExternalLink url="https://www.climatepolicyradar.org/contact">Contact Climate Policy Radar</ExternalLink>
                </li>
              </ul>
              <div className="footer__section">
                <div>Follow Climate Policy Radar</div>
                <div className="flex items-start gap-6 footer__social-links">
                  <ExternalLink url="https://twitter.com/climatepolradar">
                    <img src="/images/social/twitter.svg" alt="Twitter Logo" />
                  </ExternalLink>
                  <ExternalLink url="https://www.linkedin.com/company/climate-policy-radar">
                    <img src="/images/social/linkedIn.svg" alt="LinkedIn Logo" />
                  </ExternalLink>
                  <ExternalLink url="https://github.com/climatepolicyradar/">
                    <img src="/images/social/github.svg" alt="GitHub Logo" />
                  </ExternalLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="footer__base">
        <div className="container flex flex-1 items-end gap-10 h-full">
          <p className="mb-6">Copyright © LSE {new Date().getFullYear()}</p>
          <div className="mb-6 flex gap-10">
            <ExternalLink url="https://www.climatepolicyradar.org/privacy-policy" className="text-secondary-700 underline">
              Privacy policy
            </ExternalLink>
            <Link href={"/terms-of-use"}>
              <a className="text-secondary-700 underline">Terms of use</a>
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
