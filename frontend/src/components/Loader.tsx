const Loader = () => {
  return (
    <>
      <div className="flex items-start justify-center">
        <object
          className="radar"
          type="image/svg+xml"
          data="/images/radar-loader.svg"
          style={{ width: '80px' }}
        ></object>
      </div>
    </>
  );
};

export default Loader;
