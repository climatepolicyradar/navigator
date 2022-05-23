import Script from 'next/script';
import { useRef, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ViewSDKClient from '../api/pdf';
import Loader from './Loader';

const EmbeddedPDF = ({ document, passageIndex = null, setShowPDF = null }) => {
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

  const previewPDF = () => {
    const viewSDKClient = new ViewSDKClient();
    viewSDKClient.ready().then(() => {
      const previewFilePromise = viewSDKClient.previewFile(
        document,
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
      annotationManager.registerEventListener(function (event) {
        //console.log(event);
        if (event.type === 'ANNOTATION_ADDED') {
          //console.log('added');
        }
      });
      addAnnotations(annotationManager);
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
        source: document.document_fileid,
        selector: {
          node: {
            index,
          },
          opacity: 0.25,
          subtype: 'highlight',
          boundingBox,
          quadPoints,
          strokeColor: '#FFFF00',
          strokeWidth: 1,
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
