import { FC, useState, useEffect } from "react";

type TProps = {
  headerContent: React.ReactNode;
  isOpen?: boolean;
};

export const AccordianItem: FC<TProps> = ({ headerContent, isOpen = false, children }) => {
  const [open, setOpen] = useState(isOpen);

  useEffect(() => {
    setOpen(isOpen);
  }, [isOpen, setOpen]);

  return (
    <div className="p-4 border border-blue-400 rounded-md mx-[-4px] text-lg">
      <div className="flex flex-nowrap text-blue-700 cursor-pointer" onClick={() => setOpen(!open)} role="button">
        {headerContent}

        <div className="flex-1 flex flex-col items-end">
          <button className="text-blue-600 text-[34px] font-bold">
            {open ? "−" : "+"}
          </button>
        </div>
      </div>
      <div className={`${open ? "block" : "hidden"} accordian__content`}>{children}</div>
    </div>
  );
};
