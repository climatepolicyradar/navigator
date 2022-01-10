import Loader from './Loader';

const LoaderOverlay = () => {
  return (
    <div className="bg-semiTransWhite absolute flex items-center justify-center inset-0">
      <Loader />
    </div>
  );
};

export default LoaderOverlay;
