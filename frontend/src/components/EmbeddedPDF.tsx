import Script from 'next/script';
import { useRef, useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import ViewSDKClient from '../api/pdf';
import { dummyDocument, dummyDocument2 } from '../constants/dummyDocument';
import { useDidUpdateEffect } from '../hooks/useDidUpdateEffect';
import Loader from './Loader';

const EmbeddedPDF = ({ document, page }) => {
  const [annotationManager, setAnnotationManager] = useState(null);
  const [annotationListItems, setAnnotationListItems] = useState([]);
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
        // get APIs for gotoLocation
        adobeViewer.getAPIs().then((apis) => {
          console.log('gototlocation');
          apis
            .gotoLocation(page)
            .then(() => console.log('Success'))
            .catch((error) => console.log(error));
        });
      });
    });
  };
  const createAnnotationManager = (adobeViewer) => {
    adobeViewer.getAnnotationManager().then((annotationManager) => {
      setAnnotationManager(annotationManager);
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
  };
  const padNumber = (number) => {
    return number >= 10 ? number : number.toString().padStart(2, '0');
  };

  const generateAnnotationObject = (passage, index) => {
    const now = new Date();
    const month = padNumber(now.getMonth() + 1);
    const day = padNumber(now.getDate());
    const nowStr = `${now.getFullYear()}-${month}-${day}T${now.getHours()}:${now.getMinutes()}:00Z`;
    const coords = passage.text_block_coords;
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
          strokeWidth: 1,
          type: 'AdobeAnnoSelector',
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
  }, [containerRef]);
  useEffect(() => {
    console.log(page);
    previewPDF();
  }, [page, document]);
  return (
    <>
      <Script src="https://documentcloud.adobe.com/view-sdk/main.js" />
      {!doc ? (
        <div className="w-full flex justify-center flex-1">
          <Loader />
        </div>
      ) : (
        <div ref={containerRef} id="pdf-div" className="mt-4 px-6 flex-1">
          PDF
        </div>
      )}
    </>
  );
};
export default EmbeddedPDF;
