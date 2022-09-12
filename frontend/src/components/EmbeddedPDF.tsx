import { useRef, useMemo, useEffect } from "react";
import Script from "next/script";
import { TDocument } from "@types";
import usePDFPreview from "@hooks/usePDFPreview";
import Loader from "./Loader";

type TProps = {
  document: TDocument;
  passageIndex?: number;
};

const EmbeddedPDF = ({ document, passageIndex = null }: TProps) => {
  const containerRef = useRef();
  // Ensure the instance of the PDF client is not reset on render
  const { createPDFClient, passageIndexChangeHandler } = useMemo(() => usePDFPreview(document), [document]);

  useEffect(() => {
    if (containerRef?.current) {
      createPDFClient(passageIndex);
    }
  }, [containerRef, document]);

  useEffect(() => {
    passageIndexChangeHandler(passageIndex);
  }, [passageIndex]);

  return (
    <>
      <Script src="https://documentcloud.adobe.com/view-sdk/viewer.js" />
      {!document ? (
        <div className="w-full flex justify-center flex-1">
          <Loader />
        </div>
      ) : (
        <>
          <div ref={containerRef} id="pdf-div" className="h-full"></div>
        </>
      )}
    </>
  );
};
export default EmbeddedPDF;
