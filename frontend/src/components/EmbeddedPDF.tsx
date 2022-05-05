import Script from 'next/script';
import { useRef, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ViewSDKClient from '../api/pdf';
import { dummyDocument, dummyDocument2 } from '../constants/dummyDocument';
import Loader from './Loader';

const EmbeddedPDF = ({ document, passageIndex, setShowPDF }) => {
  const containerRef = useRef();
  const viewerConfig = {
    showDownloadPDF: true,
    showPrintPDF: true,
    showLeftHandPanel: false,
    enableAnnotationAPIs: true,
    showAnnotationTools: true,
  };
  const annotationManagerConfig = {
    showToolbar: false,
    showCommentsPanel: false,
    downloadWithAnnotations: true,
    printWithAnnotations: true,
  };
  let doc;
  if (document === null) {
    doc = dummyDocument2;
  } else {
    //const { data: doc } = document;
    doc = document.data;
  }

  const previewPDF = () => {
    const viewSDKClient = new ViewSDKClient();
    viewSDKClient.ready().then(() => {
      const previewFilePromise = viewSDKClient.previewFile(
        doc,
        'pdf-div',
        viewerConfig
      );
      previewFilePromise.then((adobeViewer) => {
        createAnnotationManager(adobeViewer);
      });
    });
  };
  const createAnnotationManager = (adobeViewer) => {
    adobeViewer.getAnnotationManager().then((annotationManager) => {
      annotationManager.setConfig(annotationManagerConfig);
      addAnnotations(annotationManager);
    });
  };
  const addAnnotations = (annotationManager) => {
    let annotations = [];
    doc.document_passage_matches.map((passage, index) => {
      const obj = generateAnnotationObject(passage, index);
      annotations.push(obj);
    });
    annotationManager.addAnnotations(annotations);
    if (passageIndex) {
      annotationManager.selectAnnotation(annotations[passageIndex].id);
    }
  };
  const padNumber = (number) => {
    return number >= 10 ? number : number.toString().padStart(2, '0');
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
      '@context': [
        'https://www.w3.org/ns/anno.jsonld',
        'https://comments.acrobat.com/ns/anno.jsonld',
      ],
      type: 'Annotation',
      id: uuidv4(),
      bodyValue: '',
      motivation: 'commenting',
      target: {
        source: doc.document_fileid,
        selector: {
          node: {
            index,
          },
          opacity: 0.25,
          subtype: 'highlight',
          boundingBox,
          quadPoints,
          strokeColor: '#FFFF00',
          strokeWidth: 0,
          type: 'AdobeAnnoSelector',
          styleClass: 'highlight',
        },
      },
      creator: {
        type: 'Person',
        name: 'Climate Policy Radar',
      },
      created: nowStr,
      modified: nowStr,
    };
  };

  useEffect(() => {
    if (containerRef?.current) {
      previewPDF();
    }
  }, [containerRef, document]);

  return (
    <>
      <Script src="https://documentcloud.adobe.com/view-sdk/main.js" />
      {!doc ? (
        <div className="w-full flex justify-center flex-1">
          <Loader />
        </div>
      ) : (
        <>
          <button
            className="ml-6 text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300"
            onClick={() => {
              setShowPDF(false);
            }}
          >
            &laquo; Back
          </button>
          <div
            ref={containerRef}
            id="pdf-div"
            className="mt-4 px-6 flex-1"
          ></div>
        </>
      )}
    </>
  );
};
export default EmbeddedPDF;
