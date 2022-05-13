import FooterLinks from './FooterLinks';

const Footer = () => {
  return (
    <footer className="h-24 dark-gradient flex items-center shrink-0">
      <div className="container">
        <FooterLinks landing={true} />
      </div>
    </footer>
  );
};
export default Footer;
