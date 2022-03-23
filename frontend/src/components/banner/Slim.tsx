interface BannerProps {
  heading: string;
}
const Slim = ({ heading }: BannerProps) => {
  return (
    <div className="banner">
      <div
        data-cy="banner-title"
        className="container h-28"
      >
        
      </div>
    </div>
  );
};
export default Slim;
