import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { useRouter } from "next/router";
import useDocumentDetail from "@hooks/useDocumentDetail";
import useSortAndStructure from "@hooks/useSortAndStructure";
import Layout from "@components/layouts/Main";
import Loader from "@components/Loader";
import TextLink from "@components/nav/TextLink";
import DocumentInfo from "@components/blocks/DocumentInfo";
import Event from "@components/blocks/Event";
import RelatedDocument from "@components/blocks/RelatedDocument";
import Tooltip from "@components/tooltip";
import { ExternalLinkIcon } from "@components/svg/Icons";
import { convertDate } from "@utils/timedate";
import { initialSummaryLength } from "@constants/document";
import { truncateString } from "../../helpers";

const DocumentCoverPage = () => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const [summary, setSummary] = useState("");
  const { t } = useTranslation("document");
  const router = useRouter();
  const structureData = useSortAndStructure();

  const documentQuery = useDocumentDetail(router.query.docId as string);
  const { isFetching } = documentQuery;
  const { data: { data: page } = {} } = documentQuery;

  console.log(page);

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
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer nofollow"
          className="text-blue-500 underline flex items-center font-medium hover:text-indigo-600 transition duration-300"
        >
          <span className="mr-1">Link to source document</span>

          <ExternalLinkIcon height="16" width="16" />
        </a>
      </p>
    );
  };

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
              <div className="md:flex">
                <div className="flex-1 my-6">
                  <h1 className="text-3xl font-medium">{page.name}</h1>
                  <div className="flex text-sm text-indigo-400 mt-3 items-center w-full">
                    <div className={`rounded-sm border border-black flag-icon-background flag-icon-${page.geography.value.toLowerCase()}`} />
                    <span className="ml-2">
                      {page.geography.display_value}, {year}
                    </span>
                    <span className="ml-8"></span>
                  </div>
                </div>
                <div className="my-6 md:pl-4 md:w-2/5 lg:w-1/4 md:ml-12 flex-shrink-0">
                  <TextLink href="/search">Back to search results</TextLink>
                </div>
              </div>
            </div>
          </div>
          <div className="container">
            <div className="md:flex">
              <section className="flex-1">
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
                <p className="text-sm mt-4">
                  <span className="font-medium">Source: </span> {page.source.name}
                </p>

                {renderSourceLink()}

                {page.related_documents.length ? (
                  <section>
                    <h2 className="text-xl flex mt-8">
                      Associated Documents
                      <div className="ml-1 text-xs">
                        <Tooltip id="docs-tt" tooltip="Other documents which are related to this document, e.g. translations, amendments, summaries, or annexes" />
                      </div>
                    </h2>
                    {page.related_documents.map((doc) => (
                      <div key={doc.related_id} className="my-8">
                        <RelatedDocument document={doc} />
                      </div>
                    ))}
                  </section>
                ) : null}
              </section>
              <section className="md:border-l md:border-blue-100 md:pl-4 mt-6 md:w-2/5 lg:w-1/4 md:ml-12 flex-shrink-0">
                <h3 className="text-xl text-blue-700">About this document</h3>
                <div className="grid grid-cols-2 gap-x-2">
                  <DocumentInfo
                    id="category-tt"
                    heading="Category"
                    text={page.category.name}
                  />
                  <DocumentInfo id="type-tt" heading="Type" text={page.type.name} />
                  {/* Topics maps to responses */}
                  {page.topics.length > 0 && (
                    <DocumentInfo
                      id="topics-tt"
                      heading="Topics"
                      list={page.topics}
                    />
                  )}
                  {page.languages.length > 0 && <DocumentInfo heading="Language" text={page.languages[0].name} />}
                </div>

                {page.keywords.length > 0 && (
                  <DocumentInfo id="keywords-tt" tooltip="Key terms relating to the content of the document" heading="Keywords" text={page.keywords[0].name} />
                )}
                {page.sectors.length > 0 && (
                  <DocumentInfo
                    id="sectors-tt"
                    tooltip="The broad areas of economic activity to which the content of the document relates, e.g. agriculture or transport. For more information, see our Methodology page"
                    heading="Sectors"
                    list={page.sectors}
                  />
                )}
                {page.instruments.length > 0 && (
                  <DocumentInfo
                    id="instruments-tt"
                    tooltip="The interventions or measures contained in the document, e.g. taxes or standards. For more information, see our Methodology page"
                    heading="Instruments"
                    list={structureData(page.instruments)}
                  />
                )}
                {page.events.length > 0 && (
                  <div className="mt-8">
                    <h4 className="text-base text-indigo-600 font-medium mb-4">Events</h4>
                    {page.events.map((event, index) => (
                      <Event event={event} key={`event${index}`} last={index === page.events.length - 1 ? true : false} />
                    ))}
                  </div>
                )}
              </section>
            </div>
          </div>
        </section>
      )}
    </Layout>
  );
};
export default DocumentCoverPage;
