import { ExternalLink } from "@components/ExternalLink";
import Link from "next/link";

const FooterLinks = ({ landing = false }) => {
  return (
    <nav>
      <div data-cy="footer-nav" className={`flex flex-col md:flex-row justify-center gap-8 md:gap-16 ${landing ? "text-white" : "text-indigo-500"}`}>
        <Link href="/methodology">
          <a className="transtion duration-300 hover:text-blue-500">Methodology</a>
        </Link>
        <Link href="/terms">
          <a className="transtion duration-300 hover:text-blue-500">Terms &amp; conditions</a>
        </Link>
        <ExternalLink url="https://climatepolicyradar.org/privacy-policy" className="transtion duration-300 hover:text-blue-500">
          Privacy Policy
        </ExternalLink>
      </div>
    </nav>
  );
};
export default FooterLinks;
