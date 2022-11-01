import { TDocument } from "@types";
import Loader from "./Loader";

type TProps = {
  document: TDocument;
  setShowPDF: (show?: boolean) => void;
  setPassageIndex: (index: number) => void;
  activeIndex?: number;
};

const PassageMatches = ({ document, setShowPDF, setPassageIndex, activeIndex }: TProps) => {
  return (
    <>
      {!document ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <>
          {document.document_passage_matches.map((item, index: number) => (
            <div
              key={item.text_block_id}
              className={`p-4 cursor-pointer border hover:bg-offwhite ${activeIndex === index ? "border-lineBorder bg-grey-200" : "border-transparent"}`}
              onClick={() => {
                setShowPDF(true);
                setPassageIndex(index);
              }}
            >
              <div className="text-s text-blue-500 ">
                <span className="font-bold">
                  {/* TODO: translation */}
                  Page {item.text_block_page} | &nbsp;
                </span>
                <span>go to page &gt;</span>
              </div>
              <p className="mt-2 text-indigo-400 font-light">{item.text}</p>
            </div>
          ))}
        </>
      )}
    </>
  );
};
export default PassageMatches;
