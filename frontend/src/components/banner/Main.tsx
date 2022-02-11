import Pill from '../Pill';
interface BannerProps {
  heading: string;
}
const Main = ({ heading }: BannerProps) => {
  return (
    <div className="banner">
      <div className="container pt-32 pb-12 md:pt-36 md:pb-20">
        <Pill text={heading} />
      </div>
    </div>
  );
};
export default Main;
