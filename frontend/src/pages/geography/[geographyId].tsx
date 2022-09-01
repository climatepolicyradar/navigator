import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { TTarget, TEvent } from "@types";
import useGeoStats from "@hooks/useGeoStats";
import useGeoSummary from "@hooks/useGeoSummary";
import Layout from "@components/layouts/Main";
import { SingleCol } from "@components/SingleCol";
import Event from "@components/blocks/Event";
import { Loading } from "@components/blocks/Loading";
import { Timeline } from "@components/blocks/Timeline";
import { CountryHeader } from "@components/blocks/CountryHeader";
import { KeyDetail } from "@components/KeyDetail";
import { Divider } from "@components/dividers/Divider";
import { RightArrowIcon } from "@components/svg/Icons";
import Button from "@components/buttons/Button";
import { RelatedDocumentFull } from "@components/blocks/RelatedDocumentFull";
import TabbedNav from "@components/nav/TabbedNav";
import TextLink from "@components/nav/TextLink";
import { LawIcon, PolicyIcon, CaseIcon, TargetIcon } from "@components/svg/Icons";
import { DOCUMENT_CATEGORIES } from "@constants/documentCategories";

type TTargets = {
  targets: TTarget[];
};

const Targets = ({ targets }: TTargets) => {
  return (
    <ul className="ml-4 list-disc list-outside">
      {targets.map((target) => (
        <li className="mb-4" key={target.target}>
          <span className="text-blue-700 text-lg">{target.target}</span>
          <span className="block">
            <span className="font-semibold mr-1">{target.group}</span>
            <span>
              | Base year: {target.base_year} | Target year: {target.target_year}
            </span>
          </span>
        </li>
      ))}
    </ul>
  );
};

const CountryPage = () => {
  const router = useRouter();
  const { geographyId } = router.query;
  const geographyQuery = useGeoStats(String(geographyId));
  const geographySummaryQuery = useGeoSummary(String(geographyId));
  const { refetch: refetchGeography, data: { data: geography } = {}, isFetching: isFetching, isError } = geographyQuery;
  const { refetch: refetchSummary, data: { data: summary } = {}, isFetching: isFetchingSummary } = geographySummaryQuery;
  const [showAllTargets, setShowAllTargets] = useState(false);
  const [selectedCategoryIndex, setselectedCategoryIndex] = useState(0);

  const hasEvents = !!summary?.events && summary?.events?.length > 0;
  const hasTargets = !!summary?.targets && summary?.targets?.length > 0;
  const hasDocuments = !!summary?.top_documents;

  const documentCategories = DOCUMENT_CATEGORIES;
  const TARGETS_SHOW = 5;

  const handleDocumentCategoryClick = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>, index: number) => {
    e.preventDefault();
    return setselectedCategoryIndex(index);
  };

  const handleDocumentSeeMoreClick = (event: React.FormEvent<HTMLButtonElement>) => {
    event.preventDefault();
    router.push("/search");
  };

  const renderEmpty = (documentType: string = "") => <p className="mt-4">{`There are no ${documentType} documents for ${geography.name}`}</p>;

  const renderDocuments = () => {
    // All
    if (selectedCategoryIndex === 0) {
      const allDocuments = summary.top_documents.Policy.concat(summary.top_documents.Law).concat(summary.top_documents.Case);
      if (allDocuments.length === 0) {
        return renderEmpty();
      }
      allDocuments.sort((a, b) => {
        return new Date(b.document_date).getTime() - new Date(a.document_date).getTime();
      });
      return allDocuments.slice(0, 5).map((doc) => (
        <div key={doc.document_id} className="mt-4 mb-10">
          <RelatedDocumentFull document={doc} />
        </div>
      ));
    }
    // Legislative
    if (selectedCategoryIndex === 1) {
      return summary.top_documents.Law.length === 0
        ? renderEmpty("Legislative")
        : summary.top_documents.Law.map((doc) => (
            <div key={doc.document_id} className="mt-4 mb-10">
              <RelatedDocumentFull document={doc} />
            </div>
          ));
    }
    // Executive
    if (selectedCategoryIndex === 2) {
      return summary.top_documents.Policy.length === 0
        ? renderEmpty("Executive")
        : summary.top_documents.Policy.map((doc) => (
            <div key={doc.document_id} className="mt-4 mb-10">
              <RelatedDocumentFull document={doc} />
            </div>
          ));
    }
    // Litigation
    if (selectedCategoryIndex === 3) {
      return (
        <div className="mt-4">
          Climate litigation case documents are coming soon to Climate Policy Radar. In the meantime, head to{" "}
          <a className="text-blue-500 transition duration-300 hover:text-indigo-600" href="https://climate-laws.org/litigation_cases" target={"_blank"}>
            climate-laws.org/litigation_cases
          </a>
        </div>
      );
    }
  };

  useEffect(() => {
    if (router.query.geographyId) {
      refetchGeography();
      refetchSummary();
    }
  }, [router.query.geographyId, refetchGeography, refetchSummary]);

  let targets = [];
  if (!!summary?.targets) targets = showAllTargets ? summary.targets : summary.targets.slice(0, TARGETS_SHOW);

  if (isFetching || isFetchingSummary) return <Loading />;

  return (
    <>
      <Layout title={`Climate Policy Radar | ${geography?.name ?? "Loading..."}`}>
        {isError || !geography ? (
          <SingleCol>
            <TextLink onClick={() => router.back()}>Go back</TextLink>
            <p>We were not able to load the data for the country.</p>
          </SingleCol>
        ) : (
          <section className="mb-8">
            <CountryHeader country={geography} />
            <SingleCol>
              <section className="grid grid-cols-2 md:grid-cols-3 gap-px rounded mb-8">
                {<KeyDetail detail="Legislation" extraDetail="from legislative branch: laws, acts, constitutions" amount={summary.document_counts.Law} icon={<LawIcon />} />}
                {<KeyDetail detail="Policies" extraDetail="from executive branch: policies, strategies, decrees, action plans" amount={summary.document_counts.Policy} icon={<PolicyIcon />} />}
                {<KeyDetail detail="Litigation" extraDetail="court cases and tribunals" amount={summary.document_counts.Case} icon={<CaseIcon />} />}
              </section>
              {hasEvents && (
                <section className="mt-12 hidden">
                  <h3 className="mb-4">Events</h3>
                  <Timeline>
                    {summary.events.map((event: TEvent, index: number) => (
                      <Event event={event} key={`event-${index}`} index={index} last={index === summary.events.length - 1 ? true : false} />
                    ))}
                  </Timeline>
                </section>
              )}

              {hasTargets && (
                <section className="mt-12">
                  <div>
                    <h3 className="flex mb-4">
                      <span className="mr-2">
                        <TargetIcon />
                      </span>
                      Targets ({summary.targets.length})
                    </h3>
                    <Targets targets={targets} />
                  </div>
                </section>
              )}
              {!showAllTargets && summary?.targets?.length > TARGETS_SHOW && (
                <div className="mt-12">
                  <Divider>
                    <Button color="secondary" wider onClick={() => setShowAllTargets(true)}>
                      See more
                    </Button>
                  </Divider>
                </div>
              )}
              {hasDocuments && (
                <>
                  <section className="mt-12">
                    <h3>Latest Documents</h3>
                    <div className="mt-4 md:flex">
                      <div className="flex-grow">
                        <TabbedNav activeIndex={selectedCategoryIndex} items={documentCategories} handleTabClick={handleDocumentCategoryClick} indent={false} />
                      </div>
                    </div>
                    {renderDocuments()}
                  </section>
                  <div className="mt-12 hidden">
                    <Divider>
                      <Button color="secondary" extraClasses="flex items-center" onClick={handleDocumentSeeMoreClick}>
                        <>
                          See more
                          <span className="ml-8">
                            <RightArrowIcon height="20" width="20" />
                          </span>
                        </>
                      </Button>
                    </Divider>
                  </div>
                </>
              )}
              {geography.legislative_process && (
                <section className="mt-12">
                  <h3 className="mb-4">Legislative Process</h3>
                  <div dangerouslySetInnerHTML={{ __html: geography.legislative_process }} />
                </section>
              )}
            </SingleCol>
          </section>
        )}
      </Layout>
    </>
  );
};

export default CountryPage;
