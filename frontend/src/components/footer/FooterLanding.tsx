import FooterLinks from './FooterLinks';

const FooterLanding = () => {
  return (
    <footer className="h-24 dark-gradient flex items-center">
      <div className="container">
        <FooterLinks landing={true} />
      </div>
    </footer>
  );
};
export default FooterLanding;
