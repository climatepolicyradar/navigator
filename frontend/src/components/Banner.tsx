import Pill from './Pill';
interface BannerProps {
  heading: string;
}
const Banner = ({ heading }: BannerProps) => {
  return (
    <div className="banner">
      <div className="banner-inner container pt-32 pb-12 md:pt-36 md:pb-20">
        <Pill text={heading} />
        <h2 className="mt-8 text-white">Submit New Action</h2>
      </div>
    </div>
  );
};
export default Banner;
