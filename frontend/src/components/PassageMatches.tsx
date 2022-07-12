import Loader from './Loader';

const PassageMatches = ({ document, setShowPDF, setPassageIndex }) => {
  return (
    <>
      {!document ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <div className="px-6">
          {document.document_passage_matches.map((item, index) => (
            <div
              key={item.text_block_id}
              className="py-4 cursor-pointer"
              onClick={() => {
                setShowPDF(true);
                setPassageIndex(index);
              }}
            >
              <span className="text-xs text-blue-500">
                {/* TODO: translation */}
                On page {item.text_block_page}
              </span>
              <p className="mt-2 text-indigo-400">...{item.text}...</p>
            </div>
          ))}
        </div>
      )}
    </>
  );
};
export default PassageMatches;
