import Script from "next/script";
import { useRef, useMemo, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import ViewSDKClient from "../api/pdf";
import Loader from "./Loader";
import { padNumber } from "../utils/timedate";
import usePDFPreview from "@hooks/usePDFPreview";

type TProps = {
  document: any;
  passageIndex?: number;
};

const EmbeddedPDF = ({ document, passageIndex = null }: TProps) => {
  const containerRef = useRef();
  // Ensure the instance of the PDF client is not reset on render
  const { createPDFClient, passageIndexChangeHandler } = useMemo(() => usePDFPreview(document), [document]);

  // TODO: refactor and enable annotation highlighting
  const annotationManagerConfig = {
    showToolbar: false,
    showCommentsPanel: false,
    downloadWithAnnotations: true,
    printWithAnnotations: true,
  };

  const createAnnotationManager = (adobeViewer) => {
    adobeViewer.getAnnotationManager().then((annotationManager) => {
      annotationManager.setConfig(annotationManagerConfig);
      annotationManager.registerEventListener(function (event) {
        //console.log(event);
        if (event.type === "ANNOTATION_ADDED") {
          //console.log('added');
        }
      });
      if (document?.document_passage_matches?.length) {
        // commented out line below until issues can be resolved
        // addAnnotations(annotationManager);
      }
    });
  };
  const addAnnotations = (annotationManager) => {
    let annotations = [];
    document.document_passage_matches.map((passage, index) => {
      const obj = generateAnnotationObject(passage, index);
      annotations.push(obj);
      //console.log(index);
      annotationManager.addAnnotations([obj]);
    });
    // annotationManager.addAnnotations(annotations);
    // console.log(document);
    // console.log(annotations);
    // console.log(passageIndex);
    if (passageIndex !== null) {
      annotationManager.selectAnnotation(annotations[passageIndex].id);
    }
  };

  const generateDate = () => {
    const now = new Date();
    const month = padNumber(now.getMonth() + 1);
    const day = padNumber(now.getDate());
    const hours = padNumber(now.getHours());
    const minutes = padNumber(now.getMinutes());
    return `${now.getFullYear()}-${month}-${day}T${hours}:${minutes}:00Z`;
  };

  const generateAnnotationObject = (passage, index) => {
    const nowStr = generateDate();
    const { text_block_coords: coords } = passage;
    const boundingBox = [...coords[0], ...coords[3]];
    const quadPoints = [...coords[0], ...coords[1], ...coords[3], ...coords[2]];

    return {
      "@context": ["https://www.w3.org/ns/anno.jsonld", "https://comments.acrobat.com/ns/anno.jsonld"],
      type: "Annotation",
      id: uuidv4(),
      bodyValue: "",
      motivation: "commenting",
      target: {
        source: document.document_fileid,
        selector: {
          node: {
            index,
          },
          opacity: 0.25,
          subtype: "highlight",
          boundingBox,
          quadPoints,
          strokeColor: "#FFFF00",
          strokeWidth: 1,
          type: "AdobeAnnoSelector",
          styleClass: "highlight",
        },
      },
      creator: {
        type: "Person",
        name: "Climate Policy Radar",
      },
      created: nowStr,
      modified: nowStr,
    };
  };

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
      <Script src="https://documentcloud.adobe.com/view-sdk/main.js" />
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
