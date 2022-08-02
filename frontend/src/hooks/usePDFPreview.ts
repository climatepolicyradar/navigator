import ViewSDKClient from "@api/pdf";
import { TDocument } from "@types";
import { PDF_SCROLL_DELAY } from "@constants/document";

export default function usePDFPreview(document: TDocument) {
  const viewerConfig = {
    showDownloadPDF: true,
    showPrintPDF: true,
    showLeftHandPanel: false,
    enableAnnotationAPIs: true,
    showAnnotationTools: true,
  };

  let viewSDKClient = null;
  let embedApi = null;

  const createPDFClient = (passage: number) => {
    viewSDKClient = new ViewSDKClient();
    viewSDKClient.ready().then(() => {
      const previewFilePromise = viewSDKClient.previewFile(document, "pdf-div", viewerConfig);
      previewFilePromise.then((adobeViewer) => {
        // createAnnotationManager(adobeViewer);
        adobeViewer.getAPIs().then((api) => {
          embedApi = api;
          passageIndexChangeHandler(passage);
        });
      });
    });
  };

  const passageIndexChangeHandler = (passage: number) => {
    if (!embedApi) {
      return;
    }
    // Keep comment for reference - PDFs do not zoom uniformly, so I have removed for now
    // embedApi.getZoomAPIs().setZoomLevel(1.5);
    // Only jump to page if a passage is selected
    if (passage === null) return;
    setTimeout(() => {
      embedApi.gotoLocation(document.document_passage_matches[passage].text_block_page);
    }, PDF_SCROLL_DELAY);
  };

  return { createPDFClient, passageIndexChangeHandler };
}
