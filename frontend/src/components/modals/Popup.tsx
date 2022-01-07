import Close from '../buttons/Close';

const Popup = ({ active, onClick, children }) => {
  return (
    <div
      style={{ position: 'fixed' }}
      className={`pointer-events-none top-0 left-0 transition duration-500 z-50 transform w-full h-full flex justify-center items-center ${
        active ? 'opacity-100' : 'opacity-0'
      }`}
    >
      <div
        className={`relative w-full m-4 rounded md:m-0 md:w-2/3 2xl:w-1/2 bg-white p-4 pt-10 md:p-8 ${
          active ? 'pointer-events-auto' : 'pointer-events-none'
        }`}
      >
        <div className="absolute top-0 right-0 mt-8 mr-8">
          <Close onClick={onClick} size="30" />
        </div>
        {children}
      </div>
    </div>
  );
};
export default Popup;
