import Pill from '../Pill';
interface BannerProps {
  heading?: string;
}
const FullHeight = ({ heading }: BannerProps) => {
  return (
    <div className="banner banner--full h-screen overflow-hidden relative flex items-center justify-center"/>
  );
};
export default FullHeight;
