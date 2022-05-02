import Close from '../buttons/Close';
interface SlideoutProps {
  children: JSX.Element | string;
  show: boolean;
  setShowSlideout(): void;
}

const Slideout = ({ children, show, setShowSlideout }) => {
  return (
    <div
      className={`${
        show ? 'translate-x-0' : 'translate-x-150'
      } transition duration-700 bg-white pt-12 z-50 shadow-2xl shadow-indigo-500 h-screen fixed top-0 right-0 w-11/12 md:w-1/2 lg:w-5/12`}
    >
      <div className="absolute top-0 right-0 mt-4 mr-4">
        <Close onClick={() => setShowSlideout(false)} />
      </div>

      <div className="h-full overflow-y-auto">{children}</div>
    </div>
  );
};
export default Slideout;
