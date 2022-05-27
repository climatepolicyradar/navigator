import FooterLinks from './FooterLinks';

const Footer = () => {
  return (
    <footer className="py-12 dark-gradient flex items-center shrink-0">
      <div className="container">
        <p className="font-medium text-lg mb-6 text-white md:text-center">
          Need help? Found a bug? Please email us at
          support@climatepolicyradar.org
        </p>
        <FooterLinks landing={true} />
      </div>
    </footer>
  );
};
export default Footer;
