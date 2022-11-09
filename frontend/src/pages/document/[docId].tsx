import React, { useEffect, useState } from "react";
import { GetServerSideProps, InferGetServerSidePropsType } from "next";
import Link from "next/link";
import Layout from "@components/layouts/Main";
import DocumentInfo from "@components/blocks/DocumentInfo";
import { Timeline } from "@components/blocks/Timeline";
import Event from "@components/blocks/Event";
import { RelatedDocument } from "@components/blocks/RelatedDocument";
import TabbedNav from "@components/nav/TabbedNav";
import { ExternalLinkIcon, GlobeIcon, PDFIcon } from "@components/svg/Icons";
import { CountryLink } from "@components/CountryLink";
import { convertDate } from "@utils/timedate";
import { initialSummaryLength } from "@constants/document";
import { truncateString } from "@helpers/index";

import { TEvent } from "@types";
import { ExternalLink } from "@components/ExternalLink";
import { ApiClient } from "@api/http-common";
import { getDocumentTitle } from "@helpers/getDocumentTitle";

const DocumentCoverPage: InferGetServerSidePropsType<typeof getServerSideProps> = ({ page }) => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const [summary, setSummary] = useState("");

  const [year] = convertDate(page?.publication_ts);

  useEffect(() => {
    if (page?.description) {
      const text = page?.description;
      if (showFullSummary) {
        setSummary(text);
      } else {
        setSummary(truncateString(text, initialSummaryLength));
      }
    }
  }, [page, showFullSummary]);

  const renderSourceLink = () => {
    let link: string;
    if (page.content_type === "application/pdf" && page.source_url.length) {
      link = page.source_url;
    } else if (page.source_url.length) {
      link = page.source_url;
    }

    if (!link) return null;

    return (
      <div className="mt-4 flex align-bottom">
        {page?.content_type.includes("pdf") && <PDFIcon height="24" width="24" />}
        {page?.content_type.includes("html") && <GlobeIcon height="24" width="24" />}
        <ExternalLink url={link} className="text-blue-500 underline font-medium hover:text-indigo-600 transition duration-300 flex ml-2">
          <span className="mr-1">{page?.content_type.includes("html") ? "Visit source website" : "See full text (opens in new tab)"}</span>
          <ExternalLinkIcon height="16" width="16" />
        </ExternalLink>
      </div>
    );
  };

  // TODO: align with BE on an approach to sources and their logos
  const sourceLogo = page?.source?.name === "CCLW" ? "grantham-logo.png" : null;
  const sourceName = page?.source?.name === "CCLW" ? "Grantham Research Institute" : page?.source?.name;

  return (
    <Layout title={page?.title}>
      <section className="mb-8">
        <div className="bg-offwhite border-solid border-lineBorder border-b">
          <div className="container">
            <div className="flex flex-col md:flex-row">
              <div className="flex-1 mt-6">
                <h1 className="text-3xl lg:smaller">{page.title}</h1>
                <div className="flex text-base text-indigo-400 mt-3 items-center w-full mb-6 font-medium">
                  <CountryLink countryCode={page.geography.value}>
                    <span className={`rounded-sm border border-black flag-icon-background flag-icon-${page.geography.value.toLowerCase()}`} />
                    <span className="ml-2">{page.geography.display_value}</span>
                  </CountryLink>
                  <span>, {year}</span>
                </div>
              </div>
              <div className="my-6 md:w-2/5 lg:w-1/4 md:pl-16 flex-shrink-0">
                <Link href="/search">
                  <a className="underline text-primary-400 hover:text-indigo-600 duration-300">Back to search results</a>
                </Link>
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

              <section className="mt-12">
                <h3>Source</h3>
                {renderSourceLink()}
              </section>

              {page.events.length > 0 && (
                <section className="mt-12">
                  <h3>Timeline</h3>
                  <Timeline>
                    {page.events.map((event: TEvent, index: number) => (
                      <React.Fragment key={`event-${index}`}>
                        <Event event={event} index={index} last={index === page.events.length - 1 ? true : false} />
                      </React.Fragment>
                    ))}
                  </Timeline>
                </section>
              )}

              {page.related_documents.length ? (
                <section className="mt-12">
                  <h3>Associated Documents</h3>
                  {page.related_documents.map((doc, i) => (
                    <div key={i + "-" + doc.slug} className="my-4">
                      <RelatedDocument document={doc} />
                    </div>
                  ))}
                </section>
              ) : null}
            </section>
            <section className="mt-6 md:w-2/5 lg:w-1/4 md:pl-12 flex-shrink-0">
              <div className="md:pl-4 md:border-l md:border-lineBorder">
                <h3>About this document</h3>
                <div className="grid grid-cols-2 gap-x-2">
                  <DocumentInfo id="category-tt" heading="Category" text={page.category.name} />
                  <DocumentInfo id="type-tt" heading="Type" text={page.type.name} />
                  {/* Topics maps to responses */}
                  {page.topics.length > 0 && <DocumentInfo id="topics-tt" heading="Topics" list={page.topics} />}
                  {page.languages.length > 0 && <DocumentInfo heading="Language" text={page.languages[0].name} />}
                </div>

                {page.keywords.length > 0 && <DocumentInfo id="keywords-tt" heading="Keywords" list={page.keywords} />}
                {page.sectors.length > 0 && <DocumentInfo id="sectors-tt" heading="Sectors" list={page.sectors} />}
                <div className="mt-8 border-t border-blue-100">
                  <h3 className="mt-4">Note</h3>
                  <div className="flex items-end my-4">
                    {sourceLogo && (
                      <div className="relative flex-shrink w-3/4 xmax-w-[40px] mr-1">
                        {/* eslint-disable-next-line @next/next/no-img-element */}
                        <img src={`/images/partners/${sourceLogo}`} alt={page.source.name} />
                      </div>
                    )}
                    {page.source.name !== "CCLW" && <p className="text-sm">{sourceName}</p>}
                  </div>
                  <p>
                    The summary of this document was written by researchers at the{" "}
                    <ExternalLink url="http://lse.ac.uk/grantham" className="text-blue-500 hover:text-indigo-600 hover:underline transition duration-300">
                      Grantham Research Institute
                    </ExternalLink>
                    . If you want to use this summary, please check{" "}
                    <ExternalLink url="https://www.lse.ac.uk/granthaminstitute/cclw-terms-and-conditions"  className="text-blue-500 hover:text-indigo-600 hover:underline transition duration-300">terms of use</ExternalLink> for citation and licensing of third party
                    data.
                  </p>
                </div>
              </div>
            </section>
          </div>
        </div>
      </section>
    </Layout>
  );
};
export default DocumentCoverPage;

export const getServerSideProps: GetServerSideProps = async (context) => {
  const id = context.params.docId;
  const client = new ApiClient(process.env.NEXT_PUBLIC_API_URL);

  const { data: page } = ({} = await client.get(`/documents/${id}`, null));
  page.title =  getDocumentTitle(page.name, page.postfix)
  return {
    props: {
      page: page,
    },
  };
};
