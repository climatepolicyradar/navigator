/* eslint-disable @next/next/no-img-element */
import Link from "next/link";
import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/Logo";

type TFooterItem = {
  title: string;
  links: TLinkItem[];
};

type TLinkItem = {
  text: string;
  url: string;
  external: boolean;
};

const navLinks: TFooterItem[] = [
  {
    title: "Navigation",
    links: [
      {
        text: "About",
        url: "/about",
        external: false,
      },
      {
        text: "Methodology",
        url: "/methodology",
        external: false,
      },
      {
        text: "Acknowledgements",
        url: "/acknowledgements",
        external: false,
      },
      {
        text: "Terms of use",
        url: "/terms-of-use",
        external: false,
      },
      {
        text: "Privacy and data protection",
        url: "https://www.lse.ac.uk/lse-information/privacy-policy",
        external: true,
      },
    ],
  },
  {
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
        text: "News and commentary",
        url: "https://www.lse.ac.uk/granthaminstitute/news-and-commentary/",
        external: true,
      },
      {
        text: "Sign up to our newsletter",
        url: "https://www.lse.ac.uk/granthaminstitute/mailing-list/ ",
        external: true,
      },
    ],
  },
];

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
          <p className="font-bold text-lg mb-2">Climate Change Laws of the World</p>
          <p className="mb-10">In partnership with the Sabin Center for Climate Change Law, Columbia Law School</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {navLinks.map((item) => (
              <div key={item.title} className="footer__section">
                <div>{item.title}</div>
                <ul>
                  {item.links.map((link) => (
                    <li key={link.text} className="mb-1">
                      {renderLink(link)}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
            <div>
              <div className="mb-10 footer__section">
                <div>Follow us</div>
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
              <div className="footer__section">
                <div>Contact</div>
                <div>Email:</div>
                <ExternalLink url="mailto:gri.cgl@lse.co.uk" className="block">
                  gri.cgl@lse.co.uk
                </ExternalLink>
                <div>Tel: +44 (0)20 7107 5027</div>
                <Link href="/contact">
                  <a>Full contact details</a>
                </Link>
              </div>
            </div>
            <div className="footer__section">
              <div className="flex gap-4">
                Powered by
                <ExternalLink className="flex text-indigo-600 mb-4" url="https://www.climatepolicyradar.org">
                  <Logo />
                </ExternalLink>
              </div>
              <p>We use AI and data science to map the world's climate policies.</p>
              <p>
                <ExternalLink url="https://www.climatepolicyradar.org">www.climatepolicyradar.org</ExternalLink>
              </p>
            </div>
          </div>
        </div>
      </div>
      <div className="footer__base">
        <div className="container flex flex-1 items-end h-full">
          <p className=" mb-6">Copyright © LSE 2022</p>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
