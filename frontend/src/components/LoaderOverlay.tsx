import Loader from './Loader';

function LoaderOverlay() {
  return (
    <div className="bg-semiTransWhite fixed flex items-center justify-center inset-0 z-10">
      <Loader />
    </div>
  );
}

export default LoaderOverlay;
