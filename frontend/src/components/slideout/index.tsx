import Close from "../buttons/Close";
import { forwardRef } from "react";

interface SlideoutProps {
  children: JSX.Element | string;
  show: boolean;
  setShowSlideout(value: boolean): void;
}

const Slideout = forwardRef(function Slideout({ children, show, setShowSlideout }: SlideoutProps, ref: React.RefObject<HTMLDivElement>) {
  return (
    <div
      ref={ref}
      className={`${
        show ? "translate-x-0" : "translate-x-[110%]"
      } transition duration-500 origin-left transform bg-white pt-14 md:pt-10 z-50 shadow-2xl shadow-black/40 h-screen fixed top-0 right-0 w-11/12`}
    >
      <div className="absolute z-10 top-0 w-full pt-1 pl-4 pr-12 border-white text-sm font-bold md:hidden">
        <div className="bg-yellow-400 rounded py-1 px-2">
          <p>Warning: PDF viewer functionality is limited on some mobile devices.</p>
        </div>
      </div>
      <div className="flex absolute z-20 top-2 right-6">
        <Close size="16" onClick={() => setShowSlideout(false)} />
      </div>

      <div className="h-full overflow-y-auto scrollbar-thumb-indigo-300 scrollbar-thin scrollbar-track-white scrollbar-thumb-rounded-full mr-2">{children}</div>
    </div>
  );
});
export default Slideout;
