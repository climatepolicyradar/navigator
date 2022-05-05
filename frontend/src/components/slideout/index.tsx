import Close from '../buttons/Close';
interface SlideoutProps {
  children: JSX.Element | string;
  show: boolean;
  setShowSlideout(value: boolean): void;
}

const Slideout = ({ children, show, setShowSlideout }: SlideoutProps) => {
  return (
    <div
      className={`${
        show ? 'translate-x-0' : 'translate-x-150'
      } transition duration-700 bg-white pt-16 z-50 shadow-2xl shadow-black/40 h-screen fixed top-0 right-0 w-11/12 md:w-1/2 lg:w-5/12`}
    >
      <div className="absolute top-0 right-0 mt-4 mr-4">
        <Close size="16" onClick={() => setShowSlideout(false)} />
      </div>

      <div className="h-full overflow-y-auto scrollbar scrollbar-thumb-indigo-300 scrollbar-thin scrollbar-track-white scrollbar-thumb-rounded-full mr-2">
        {children}
      </div>
    </div>
  );
};
export default Slideout;