import ViewSDKClient from "@api/pdf";
import { TDocument } from "@types";
import { PDF_SCROLL_DELAY } from "@constants/document";

function generateHighlights(document: TDocument) {
  const date = new Date();
  return document.document_passage_matches.map((passage) => {
    return {
      "@context": ["https://www.w3.org/ns/anno.jsonld", "https://comments.acrobat.com/ns/anno.jsonld"],
      type: "Annotation",
      id: passage.text_block_id,
      bodyValue: "",
      motivation: "commenting",
      target: {
        source: document.document_fileid,
        selector: {
          node: {
            index: passage.text_block_page - 1,
          },
          subtype: "highlight",
          // WE CAN ASSUME BLOCK_COORDS IS ALWAYS LENGTH 4
          // format [xmin, ymin, xmax, ymax]
          boundingBox: [passage.text_block_coords[0][0], passage.text_block_coords[0][1], passage.text_block_coords[1][0], passage.text_block_coords[2][1]],
          // format [Xmin, Ymin, Xmax, Ymin, Xmax, Ymax, Xmin, Ymax]
          quadPoints: [
            passage.text_block_coords[0][0],
            passage.text_block_coords[0][1],
            passage.text_block_coords[1][0],
            passage.text_block_coords[0][1],
            passage.text_block_coords[0][0],
            passage.text_block_coords[2][1],
            passage.text_block_coords[1][0],
            passage.text_block_coords[2][1],
          ],
          styleClass: "body-value-css",
          type: "AdobeAnnoSelector",
          strokeColor: "#FFFF00",
          strokeWidth: 1,
          opacity: 0.25,
        },
      },
      creator: {
        type: "Person",
        name: "Climate Policy Radar",
      },
      created: date.toISOString(),
      modified: date.toISOString(),
    };
  });
}

export default function usePDFPreview(document: TDocument) {
  const viewerConfig = {
    showDownloadPDF: true,
    showPrintPDF: true,
    showLeftHandPanel: false,
    enableAnnotationAPIs: true,
    includePDFAnnotations: true,
    showAnnotationTools: true,
    defaultViewMode: "FIT_PAGE",
  };

  let viewSDKClient = null;
  let embedApi = null;

  const createPDFClient = (passage: number) => {
    viewSDKClient = new ViewSDKClient();
    viewSDKClient.ready().then(() => {
      const previewFilePromise = viewSDKClient.previewFile(document, "pdf-div", viewerConfig);
      previewFilePromise.then((adobeViewer) => {
        adobeViewer.getAPIs().then((api: any) => {
          embedApi = api;
          passageIndexChangeHandler(passage);
        });
        adobeViewer.getAnnotationManager().then((annotationManager: any) => {
          annotationManager.setConfig({ showToolbar: false, showCommentsPanel: false, downloadWithAnnotations: true, printWithAnnotations: true });
          annotationManager.addAnnotations(generateHighlights(document));
        });
      });
    });
  };

  const passageIndexChangeHandler = (passageIndex: number) => {
    if (!embedApi) {
      return;
    }
    if (passageIndex === null) return;
    setTimeout(() => {
      embedApi.gotoLocation(document.document_passage_matches[passageIndex].text_block_page);
    }, PDF_SCROLL_DELAY);
  };

  return { createPDFClient, passageIndexChangeHandler };
}
