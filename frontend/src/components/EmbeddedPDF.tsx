import { dummyDocument } from '../constants/dummyDocument';

const EmbeddedPDF = ({ document, showPDF, setShowPDF }) => {
  let doc;
  if (document === null) {
    doc = dummyDocument;
  } else {
    //const { data: doc } = document;
    doc = document.data;
  }
  console.log(doc);
  return <p>PDF view</p>;
};
export default EmbeddedPDF;
