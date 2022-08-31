import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
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
import { RelatedDocument } from "@components/blocks/RelatedDocument";
import TabbedNav from "@components/nav/TabbedNav";
import Sort from "@components/filters/Sort";
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

  const handleDocumentCategoryClick = (e: any) => {
    return false;
  };
  const handleSortClick = (e: any) => {
    return false;
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
                {<KeyDetail detail="Legislative" extraDetail="Laws, Decrees" amount={summary.document_counts.Law} icon={<LawIcon />} />}
                {<KeyDetail detail="Executive" extraDetail="Policies" amount={summary.document_counts.Policy} icon={<PolicyIcon />} />}
                {<KeyDetail detail="Litigation" extraDetail="Cases" amount={summary.document_counts.Case} icon={<CaseIcon />} />}
              </section>
              {hasEvents && (
                <section className="mt-12">
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
                    <h3>Documents</h3>
                    <div className="mt-4 md:flex">
                      <div className="flex-grow">
                        <TabbedNav activeIndex={selectedCategoryIndex} items={documentCategories} handleTabClick={handleDocumentCategoryClick} indent={false} />
                      </div>
                      <div className="mt-4 md:-mt-2 md:ml-2 lg:ml-8 md:mb-2 flex items-center">
                        <Sort defaultValue="date:desc" updateSort={handleSortClick} browse />
                      </div>
                    </div>
                    {summary.top_documents.Case.map((doc) => (
                      <div key={doc.document_id} className="mt-4 mb-10">
                        {/* <RelatedDocument document={doc} /> */}
                        {doc.document_name}
                      </div>
                    ))}
                  </section>
                  <div className="mt-12">
                    <Divider>
                      <Button color="secondary" extraClasses="flex items-center">
                        <Link href="/search">
                          <>
                            See more
                            <span className="ml-8">
                              <RightArrowIcon height="20" width="20" />
                            </span>
                          </>
                        </Link>
                      </Button>
                    </Divider>
                  </div>
                </>
              )}
              {geography.legislative_process && (
                <>
                  <h3 className="mb-4">Legislative Process</h3>
                  <div dangerouslySetInnerHTML={{ __html: geography.legislative_process }} />
                </>
              )}
            </SingleCol>
          </section>
        )}
      </Layout>
    </>
  );
};

export default CountryPage;
