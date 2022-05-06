import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import useDocument from '../../hooks/useDocument';
import EmbeddedPDF from '../../components/EmbeddedPDF';
import Loader from '../../components/Loader';
import Link from 'next/link';
import BackLink from '../../components/nav/BackLink';

const PDFView = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const router = useRouter();
  const document: any = useDocument();
  useEffect(() => {
    console.log(document);
    if (!document.data) router.push('/');
  }, []);
  return (
    <>
      {!document ? (
        <div className="w-full flex justify-center flex-1">
          <Loader />
        </div>
      ) : (
        <Layout
          title={`Navigator | ${t('Law and Policy Search PDF View')}`}
          heading={t('Law and Policy Search PDF View')}
          screenHeight={true}
        >
          <div className="container mt-2">
            <h1 className="text-2xl font-medium">
              {document?.data?.document_name}
            </h1>
            <BackLink href="/search" text="Back to search results" />
          </div>
          <section className="mt-4 flex-1">
            <div className="h-full container">
              {/* TODO: pass in real document when api and docs are ready */}
              <EmbeddedPDF document={null} />
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};
export default PDFView;
