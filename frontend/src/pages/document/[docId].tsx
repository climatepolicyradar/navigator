import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect, useState } from 'react';
import Loader from '../../components/Loader';
import Link from 'next/link';
import TextLink from '../../components/nav/TextLink';
import { truncateString } from '../../helpers';
import SearchResult from '../../components/blocks/SearchResult';
import { dummyDocument, dummyDocument2 } from '../../constants/dummyDocument';
import DocumentInfo from '../../components/blocks/DocumentInfo';
import Event from '../../components/blocks/Event';
import useDocumentDetail from '../../hooks/useDocumentDetail';
import RelatedDocument from '../../components/blocks/RelatedDocument';

const DocumentCoverPage = () => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const { t, i18n, ready } = useTranslation('searchStart');
  const router = useRouter();

  const {
    data: page,
    isFetching,
    isError,
    error,
  }: any = useDocumentDetail(router.query.docId as string);

  return (
    <Layout title={`Navigator | Document title`}>
      {isFetching ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        // TODO: translate all UI text
        <section className="mb-8">
          <div className="container">
            <TextLink href="/search">
              <span className="text-lg">&laquo;</span>Back to search results
            </TextLink>{' '}
            <span className="mx-1">|</span>
            <TextLink href="/">Download PDF</TextLink>
            <h1 className="mt-6 text-3xl font-medium">{page.name}</h1>
            <div className="flex text-xs text-indigo-400 mt-3">
              <div
                className={`rounded-sm border border-black flag-icon-background flag-icon-usa`}
              />
              <span className="ml-2">United States of America</span>
              <span className="ml-6">2009</span>
            </div>
            <div className="md:flex">
              <section className="flex-1">
                <section className="mt-6">
                  {showFullSummary
                    ? page.description
                    : truncateString(page.description, 350)}
                </section>
                <section className="mt-6 flex justify-end">
                  {showFullSummary ? (
                    <button
                      onClick={() => setShowFullSummary(false)}
                      className="text-blue-500 font-medium"
                    >
                      Collapse
                    </button>
                  ) : (
                    <button
                      onClick={() => setShowFullSummary(true)}
                      className="text-blue-500 font-medium"
                    >
                      Show full summary
                    </button>
                  )}
                </section>
                <section>
                  <h2 className="text-xl">Associated Documents</h2>
                  {page.related_documents.map((doc) => (
                    <div key={doc.related_id} className="my-8">
                      <RelatedDocument
                        document={doc}
                        onClick={() =>
                          router.push(`/document/${doc.related_id}`)
                        }
                      />
                    </div>
                  ))}
                </section>
              </section>
              <section className="border-l border-blue-100 pl-4 mt-6 md:w-2/5 lg:w-4/12 md:ml-12 flex-shrink-0">
                <h3 className="text-xl text-indigo-400">
                  Further information about this document
                </h3>
                <DocumentInfo heading="Category" text={page.category.name} />
                <DocumentInfo heading="Type" text={page.type.name} />
                {/* Topics maps to responses */}
                <DocumentInfo heading="Topics" list={page.topics} />
                <DocumentInfo
                  heading="Language"
                  text={page.languages[0].name}
                />
                {/* <DocumentInfo heading="Keywords" text={page.keywords} /> */}
                <DocumentInfo heading="Sectors" list={page.sectors} />
                <DocumentInfo heading="Instruments" list={page.instruments} />
                <div className="mt-8">
                  <h4 className="text-base text-indigo-600 font-medium mb-4">
                    Events
                  </h4>
                  {page.events.map((event, index) => (
                    <Event
                      event={event}
                      key={`event${index}`}
                      last={index === page.events.length - 1 ? true : false}
                    />
                  ))}
                </div>
              </section>
            </div>
          </div>
        </section>
      )}
    </Layout>
  );
};
export default DocumentCoverPage;
