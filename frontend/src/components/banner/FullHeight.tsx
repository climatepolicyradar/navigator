import Pill from '../Pill';
interface BannerProps {
  heading?: string;
}
const FullHeight = ({ heading }: BannerProps) => {
  return (
    <div className="banner banner--full h-screen overflow-hidden relative">
      <div data-cy="banner-title" className="container pt-40 md:pt-28">
        {heading && <Pill text={heading} />}
      </div>
    </div>
  );
};
export default FullHeight;
