import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import useDocumentDetail from "@hooks/useDocumentDetail";
import useSortAndStructure from "@hooks/useSortAndStructure";
import Layout from "@components/layouts/Main";
import Loader from "@components/Loader";
import TextLink from "@components/nav/TextLink";
import DocumentInfo from "@components/blocks/DocumentInfo";
import { Timeline } from "@components/blocks/Timeline";
import Event from "@components/blocks/Event";
import { RelatedDocument } from "@components/blocks/RelatedDocument";
import TabbedNav from "@components/nav/TabbedNav";
import { ExternalLinkIcon } from "@components/svg/Icons";
import { convertDate } from "@utils/timedate";
import { initialSummaryLength } from "@constants/document";
import { truncateString } from "@helpers/index";

import { TEvent } from "@types";

const DocumentCoverPage = () => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const [summary, setSummary] = useState("");
  const router = useRouter();
  const structureData = useSortAndStructure();

  const documentQuery = useDocumentDetail(router.query.docId as string);
  const { data: { data: page } = {}, isFetching } = documentQuery;

  const [year] = convertDate(page?.publication_ts);

  useEffect(() => {
    if (page?.description) {
      toggleSummary();
    }
  }, [page, showFullSummary]);

  useEffect(() => {
    if (router?.query.docId) {
      documentQuery.refetch();
    }
  }, [router.query]);

  const toggleSummary = () => {
    const text = page?.description;
    if (showFullSummary) {
      setSummary(text);
    } else {
      setSummary(truncateString(text, initialSummaryLength));
    }
  };

  const renderSourceLink = () => {
    let link: string;
    if (page.content_type === "application/pdf" && page.url.length) {
      link = page.url;
    } else if (page.source_url.length) {
      link = page.source_url;
    }

    if (!link) return null;

    return (
      <p className="mt-4">
        <a href={link} target="_blank" rel="noopener noreferrer nofollow" className="text-blue-500 underline font-medium hover:text-indigo-600 transition duration-300">
          <span className="mr-1">Link to source document</span>
          <span className="inline-block">
            <ExternalLinkIcon height="16" width="16" />
          </span>
        </a>
      </p>
    );
  };

  // TODO: align with BE on an approach to sources and their logos
  const sourceLogo = page?.source?.name === "CCLW" ? "lse-logo.png" : null;

  return (
    <Layout title={`Climate Policy Radar | Document title`}>
      {isFetching || !page?.name ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        <section className="mb-8">
          <div className="bg-offwhite border-solid border-blue-200 border-b">
            <div className="container">
              <div className="flex flex-col md:flex-row">
                <div className="flex-1 mt-6">
                  <h1 className="text-3xl lg:smaller">{page.name}</h1>
                  <div className="flex text-sm text-indigo-400 mt-3 items-center w-full mb-6">
                    <div className={`rounded-sm border border-black flag-icon-background flag-icon-${page.geography.value.toLowerCase()}`} />
                    <span className="ml-2">
                      {page.geography.display_value}, {year}
                    </span>
                  </div>
                </div>
                <div className="my-6 md:w-2/5 lg:w-1/4 md:pl-16 flex-shrink-0">
                  <TextLink href="/search">Back to search results</TextLink>
                </div>
              </div>
              <TabbedNav activeIndex={0} items={["Overview"]} handleTabClick={() => false} showBorder={false} />
            </div>
          </div>
          <div className="container">
            <div className="md:flex">
              <section className="flex-1 md:w-0">
                <section className="mt-6 text-content">
                  <div dangerouslySetInnerHTML={{ __html: summary }} />
                </section>
                {page.description.length > initialSummaryLength && (
                  <section className="mt-6 flex justify-end">
                    {showFullSummary ? (
                      <button onClick={() => setShowFullSummary(false)} className="text-blue-500 font-medium">
                        Collapse
                      </button>
                    ) : (
                      <button onClick={() => setShowFullSummary(true)} className="text-blue-500 font-medium">
                        Show full summary
                      </button>
                    )}
                  </section>
                )}

                {page.events.length > 0 && (
                  <section className="mt-12">
                    <h3>Timeline</h3>
                    <Timeline>
                      {page.events.map((event: TEvent, index: number) => (
                        <Event event={event} key={`event-${index}`} index={index} last={index === page.events.length - 1 ? true : false} />
                      ))}
                    </Timeline>
                  </section>
                )}

                {page.related_documents.length ? (
                  <section className="mt-12">
                    <h3>Associated Documents</h3>
                    {page.related_documents.map((doc) => (
                      <div key={doc.related_id} className="my-4">
                        <RelatedDocument document={doc} />
                      </div>
                    ))}
                  </section>
                ) : null}
              </section>
              <section className="mt-6 md:w-2/5 lg:w-1/4 md:pl-12 flex-shrink-0">
                <div className="md:pl-4 md:border-l md:border-blue-100">
                  <h3 className="text-blue-700">About this document</h3>
                  <div className="grid grid-cols-2 gap-x-2">
                    <DocumentInfo id="category-tt" heading="Category" text={page.category.name} />
                    <DocumentInfo id="type-tt" heading="Type" text={page.type.name} />
                    {/* Topics maps to responses */}
                    {page.topics.length > 0 && <DocumentInfo id="topics-tt" heading="Topics" list={page.topics} />}
                    {page.languages.length > 0 && <DocumentInfo heading="Language" text={page.languages[0].name} />}
                  </div>

                  {page.keywords.length > 0 && <DocumentInfo id="keywords-tt" heading="Keywords" list={page.keywords} />}
                  {page.sectors.length > 0 && <DocumentInfo id="sectors-tt" heading="Sectors" list={page.sectors} />}
                  {page.instruments.length > 0 && <DocumentInfo id="instruments-tt" heading="Instruments" list={structureData(page.instruments)} bulleted={true} />}
                  <div className="mt-8 border-t border-blue-100">
                    <h3 className="text-blue-700 mt-4">Source</h3>
                    <div className="flex items-end mt-4">
                      {sourceLogo && (
                        <div className="relative flex-shrink max-w-[40px] mr-1">
                          <img src={`/images/partners/${sourceLogo}`} alt={page.source.name} />
                        </div>
                      )}
                      <p className="text-sm">{page.source.name}</p>
                    </div>
                    {renderSourceLink()}
                  </div>
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
