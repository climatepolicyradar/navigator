import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import useDocument from '../../hooks/useDocument';
import EmbeddedPDF from '../../components/EmbeddedPDF';
import Loader from '../../components/Loader';
import Link from 'next/link';

const PDFView = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const router = useRouter();
  const document = useDocument();
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
        >
          <div className="container mt-2">
            <Link href="/search">
              <a className="ml-6 text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300">
                &laquo; Back to search results
              </a>
            </Link>
          </div>
          <section className="flex-1">
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
