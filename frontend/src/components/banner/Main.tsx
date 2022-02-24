import Pill from '../Pill';
interface BannerProps {
  heading: string;
}
const Main = ({ heading }: BannerProps) => {
  return (
    <div className="banner">
      <div
        data-cy="banner-title"
        className="container pt-40 md:pt-28 pb-12 md:pb-20"
      >
        <Pill text={heading} />
      </div>
    </div>
  );
};
export default Main;
