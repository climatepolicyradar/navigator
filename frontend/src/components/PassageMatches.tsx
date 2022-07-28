import { TDocument } from "@types";
import Loader from "./Loader";

type TProps = {
  document: TDocument;
  setShowPDF: (show: boolean) => void;
  setPassageIndex: (index: number) => void;
};

const PassageMatches = ({ document, setShowPDF, setPassageIndex }: TProps) => {
  return (
    <>
      {!document ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <div className="px-6">
          {document.document_passage_matches.map((item, index: number) => (
            <div
              key={item.text_block_id}
              className="py-4 cursor-pointer"
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
              <p className="mt-2 text-indigo-400">{item.text}</p>
            </div>
          ))}
        </div>
      )}
    </>
  );
};
export default PassageMatches;
