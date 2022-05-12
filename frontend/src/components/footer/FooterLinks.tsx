import Link from 'next/link';

const FooterLinks = ({ landing = false }) => {
  return (
    <div
      className={`flex justify-center gap-8 md:gap-16 ${
        landing ? 'text-white' : 'text-indigo-500'
      }`}
    >
      <Link href="/terms">
        <a className="transtion duration-300 hover:text-blue-500">
          Terms &amp; conditions
        </a>
      </Link>
      <Link href="/support">
        <a className="transtion duration-300 hover:text-blue-500">Support</a>
      </Link>
      <Link href="/feedback">
        <a className="transtion duration-300 hover:text-blue-500">Feedback</a>
      </Link>
    </div>
  );
};
export default FooterLinks;
