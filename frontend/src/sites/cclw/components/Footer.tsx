import Link from "next/link";
import { ExternalLink } from "@components/ExternalLink";

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
        url: "/",
        external: false,
      },
      {
        text: "Methodology",
        url: "/",
        external: false,
      },
      {
        text: "Collaborations & Acknowledgements",
        url: "/",
        external: false,
      },
      {
        text: "Terms of use",
        url: "/",
        external: false,
      },
      {
        text: "Policy & data protection",
        url: "/",
        external: false,
      },
    ],
  },
  {
    title: "Grantham Research Institute",
    links: [
      {
        text: "Governance & legislation research theme",
        url: "/",
        external: true,
      },
      {
        text: "Publications",
        url: "/",
        external: true,
      },
      {
        text: "News & commentray",
        url: "/",
        external: true,
      },
      {
        text: "Research topics",
        url: "/",
        external: true,
      },
      {
        text: "Events",
        url: "/",
        external: true,
      },
      {
        text: "People",
        url: "/",
        external: true,
      },
      {
        text: "Mailing list",
        url: "/",
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
    <footer className="flex flex-col bg-grey-400">
      <div className="py-12">
        <div className="container">
          <p className="font-bold text-lg mb-2">Climate Change Laws of the World</p>
          <p className="mb-10">In partnership with the Sabin Center for Climate Change Law, Columbia Law School</p>
          <div className="grid grid-cols-4 gap-4">
            {navLinks.map((item) => (
              <div key={item.title} className="footer-section">
                <div>{item.title}</div>
                <ul>
                  {item.links.map((link) => (
                    <li key={link.text} className="mb-1 footer-link">
                      {renderLink(link)}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
            <div>
              <div className="mb-10 footer-section">
                <div>Follow us</div>
                <div className="flex items-start gap-6">
                  <span>Tw</span>
                  <span>Fb</span>
                  <span>Yt</span>
                  <span>Ln</span>
                </div>
              </div>
              <div className="footer-section">
                <div>Contact</div>
                <div>Email:</div>
                <ExternalLink url="mailto:gri.cgl@lse.co.uk" className="block">gri.cgl@lse.co.uk</ExternalLink>
                <div>Tel: +44 (0)20 7107 5027</div>
                <ExternalLink url="/">Full contact details</ExternalLink>
              </div>
            </div>
            <div className="footer-section">
              <div>Power by CPR</div>
            </div>
          </div>
        </div>
      </div>
      <div className="footer-base">
        <div className="container flex flex-1 items-end h-full">
          <p className=" mb-6">Copyright © LSE 2022</p>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
