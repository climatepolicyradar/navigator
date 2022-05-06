import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect, useState } from 'react';
import Loader from '../../components/Loader';
import Link from 'next/link';
import BackLink from '../../components/nav/BackLink';
import { truncateString } from '../../helpers';
import SearchResult from '../../components/text-blocks/SearchResult';
import { dummyDocument, dummyDocument2 } from '../../constants/dummyDocument';
import DocumentInfo from '../../components/text-blocks/DocumentInfo';
import Event from '../../components/text-blocks/Event';

const DocumentCoverPage = () => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const { t, i18n, ready } = useTranslation('searchStart');
  const { cover_page } = dummyDocument;
  const router = useRouter();

  return (
    <Layout title={`Navigator | Document title`}>
      {/* TODO: translate all UI text on page */}
      <div className="container mt-2"></div>
      <section className="mb-8">
        <div className="container">
          <BackLink href="/search" text="Back to search results" />
          <h1 className="mt-6 text-3xl font-medium">
            Energy Independence and Security Act of 2007
          </h1>
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
                  ? cover_page.summary
                  : truncateString(cover_page.summary, 350)}
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
                <div className="my-16 mt-6">
                  <SearchResult
                    document={dummyDocument}
                    showAllOptions={false}
                    onClick={() =>
                      router.push(`/document/${dummyDocument.document_id}`)
                    }
                  />
                </div>
                <div className="my-4">
                  <SearchResult
                    document={dummyDocument2}
                    showAllOptions={false}
                    onClick={() =>
                      router.push(`/document/${dummyDocument2.document_id}`)
                    }
                  />
                </div>
              </section>
            </section>
            {/* <section className="mt-6 md:w-1/4 md:ml-12 flex-shrink-0 bg-sky p-4 rounded-lg"> */}
            <section className="border-l border-blue-100 pl-4 mt-6 md:w-2/5 lg:w-4/12 md:ml-12 flex-shrink-0">
              <h3 className="text-xl text-indigo-400">
                Further information about this document
              </h3>
              <DocumentInfo heading="Category" text={cover_page.category} />
              <DocumentInfo heading="Type" text={cover_page.type} />
              <DocumentInfo heading="Topics" list={cover_page.topics} />
              <DocumentInfo heading="Language" text={cover_page.language} />
              <DocumentInfo heading="Keywords" text={cover_page.keywords} />
              <DocumentInfo heading="Sectors" list={cover_page.sectors} />
              <DocumentInfo
                heading="Instruments"
                list={cover_page.instruments}
              />
              <div className="mt-8">
                <h4 className="text-base text-indigo-600 font-medium mb-4">
                  Events
                </h4>
                {cover_page.events.map((event, index) => (
                  <Event
                    event={event}
                    key={`event${index}`}
                    last={index === cover_page.events.length - 1 ? true : false}
                  />
                ))}
              </div>
            </section>
          </div>
        </div>
      </section>
    </Layout>
  );
};
export default DocumentCoverPage;
