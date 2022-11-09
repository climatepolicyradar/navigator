import { useRouter } from "next/router";
import Layout from "../../components/layouts/Main";
import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import useDocument from "../../hooks/useDocument";
import EmbeddedPDF from "../../components/EmbeddedPDF";
import Loader from "../../components/Loader";
import useDocumentDetail from "../../hooks/useDocumentDetail";
import TextLink from "../../components/nav/TextLink";
import { v4 as uuidv4 } from "uuid";
import { getDocumentTitle } from "@helpers/getDocumentTitle";

const PDFView = () => {
  const [document, setDocument] = useState(null);
  const { t, i18n, ready } = useTranslation("searchStart");
  const router = useRouter();
  // get selected document to show passage matches
  const { data: selectedDoc }: any = useDocument();
  // get document detail in case no document was selected
  const documentQuery = useDocumentDetail(router.query.docId as string);
  const { isFetching, isError, error, data: { data: documentDetail } = {} } = documentQuery;

  useEffect(() => {
    setDocument(selectedDoc);
    // if no selected document, use doc detail instead
    // and map document_url and document_name to url and name
    // add document_fileid for Adobe PDF embed
    if (selectedDoc === null && documentDetail) {
      const doc = {
        ...documentDetail,
        document_url: documentDetail.url,
        document_name: documentDetail.name,
        document_fileid: uuidv4(),
      };
      setDocument(doc);
    }
  }, [selectedDoc, documentDetail]);
  const title = getDocumentTitle(document.document_name, document.document_postfix);
  return (
    <>
      {!document ? (
        <div className="w-full flex justify-center flex-1">
          <Loader />
        </div>
      ) : (
        <Layout title={title ?? "Loading..."} heading={t("Law and Policy Search PDF View")} screenHeight={true}>
          <div className="container mt-2">
            <h1 className="text-2xl font-medium">{title}</h1>
            {/* TODO: translate below text */}
            <TextLink href="/search">
              <span className="text-lg">&laquo;</span>Back to search results
            </TextLink>
          </div>
          <section className="mt-4 flex-1">
            <div className="container pdf-container">
              <EmbeddedPDF document={document} />
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};
export default PDFView;
