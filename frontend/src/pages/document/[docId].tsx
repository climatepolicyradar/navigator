import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect, useState } from 'react';
import Loader from '../../components/Loader';
import TextLink from '../../components/nav/TextLink';
import { truncateString } from '../../helpers';
import DocumentInfo from '../../components/blocks/DocumentInfo';
import Event from '../../components/blocks/Event';
import useDocumentDetail from '../../hooks/useDocumentDetail';
import RelatedDocument from '../../components/blocks/RelatedDocument';
import Tooltip from '../../components/tooltip';
import { convertDate } from '../../utils/timedate';
import { DownloadPDFIcon } from '../../components/svg/Icons';

const DocumentCoverPage = () => {
  const [showFullSummary, setShowFullSummary] = useState(false);
  const [summary, setSummary] = useState('');
  const { t, i18n, ready } = useTranslation('searchStart');
  const router = useRouter();
  const collapsedLength = 700;

  const documentQuery = useDocumentDetail(router.query.docId as string);

  const { isFetching, isError, error, data } = documentQuery;
  const { data: { data: page } = {} } = documentQuery;

  const [year, day, month] = convertDate(page?.publication_ts);

  const toggleSummary = () => {
    const text = page?.description;
    if (showFullSummary) {
      setSummary(text);
    } else {
      setSummary(truncateString(text, collapsedLength));
    }
  };

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

  return (
    <Layout title={`Climate Policy Radar | Document title`}>
      {isFetching || !page?.name ? (
        <div className="w-full flex justify-center h-96">
          <Loader />
        </div>
      ) : (
        // TODO: translate all UI text
        <section className="mt-4 mb-8">
          <div className="container">
            <TextLink href="/search">
              <span>&laquo;</span> Back to search results
            </TextLink>

            <h1 className="mt-6 text-3xl font-medium">{page.name}</h1>
            <div className="flex text-xs text-indigo-400 mt-3 items-center w-full">
              <div
                className={`rounded-sm border border-black flag-icon-background flag-icon-${page.geography.value.toLowerCase()}`}
              />
              <span className="ml-2">{page.geography.display_value}</span>
              <div className="ml-1">
                <Tooltip
                  id="date-tt"
                  tooltip="The jurisdiction in which the document was published. For more information, see our Methodology page"
                />
              </div>
              <span className="ml-6">{`${year}/${day}/${month}`}</span>
              <div className="ml-1">
                <Tooltip
                  id="juris-tt"
                  tooltip="The year in which the document was first published"
                />
              </div>
              {/* Note: link to non-pdf document is page.source_url */}
              {page.content_type === 'application/pdf' && (
                <div className="ml-6">
                  <a
                    target="_blank"
                    className="bg-blue-500 rounded-full py-2 px-4 text-white flex items-center transition duration-300 hover:bg-indigo-600"
                    href={page.url}
                  >
                    <span className="sr-only">Download PDF</span>
                    <DownloadPDFIcon height="24" width="24" />{' '}
                    <span className="ml-1">Download</span>
                  </a>
                </div>
              )}
            </div>
            <div className="md:flex">
              <section className="flex-1">
                <section className="mt-6 text-content">
                  <div dangerouslySetInnerHTML={{ __html: summary }} />
                </section>
                {page.description.length > collapsedLength && (
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
                )}

                {page.related_documents.length ? (
                  <section>
                    <h2 className="text-xl flex mt-8">
                      Associated Documents
                      <div className="ml-1 text-xs">
                        <Tooltip
                          id="docs-tt"
                          tooltip="Other documents which are related to this document, e.g. translations, amendments, summaries, or annexes"
                        />
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
              <section className="md:border-l md:border-blue-100 md:pl-4 mt-6 md:w-2/5 lg:w-4/12 md:ml-12 flex-shrink-0">
                <h3 className="text-xl text-indigo-400">
                  Further information about this document
                </h3>
                <DocumentInfo
                  id="category-tt"
                  tooltip="Whether the document is enacted by an executive branch of government (for example, a ministry or the president) or by a legislative branch of government (for example, parliament or congress)"
                  heading="Category"
                  text={page.category.name}
                />
                <DocumentInfo
                  id="type-tt"
                  tooltip="What type of document it is - e.g. law, strategy, or decree"
                  heading="Type"
                  text={page.type.name}
                />
                {/* Topics maps to responses */}
                {page.topics.length > 0 && (
                  <DocumentInfo
                    id="topics-tt"
                    tooltip="Broad areas of climate action contained in the document, e.g. mitigation or adaptation. For more information, see our Methodology page"
                    heading="Topics"
                    list={page.topics}
                  />
                )}

                {page.languages.length > 0 && (
                  <DocumentInfo
                    heading="Language"
                    text={page.languages[0].name}
                  />
                )}
                {page.keywords.length > 0 && (
                  <DocumentInfo
                    id="keywords-tt"
                    tooltip="Key terms relating to the content of the document"
                    heading="Keywords"
                    text={page.keywords[0].name}
                  />
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
                    list={page.instruments}
                  />
                )}
                {page.events.length > 0 && (
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
