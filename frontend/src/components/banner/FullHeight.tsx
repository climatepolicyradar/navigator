import Pill from '../Pill';
interface BannerProps {
  heading: string;
}
const FullHeight = ({ heading }: BannerProps) => {
  return (
    <div className="banner h-screen overflow-hidden relative">
      <div className="container pt-40 md:pt-28">
        <Pill text={heading} />
      </div>
    </div>
  );
};
export default FullHeight;
