import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import { TTarget, TEvent } from "@types";
import useGeoStats from "@hooks/useGeoStats";
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
  const { countryId } = router.query;
  const countryQuery = useGeoStats(String(countryId));
  const { refetch, data: { data: country } = {}, isFetching: isFetching, isError } = countryQuery;
  const [showAllTargets, setShowAllTargets] = useState(false);
  const [selectedCategoryIndex, setselectedCategoryIndex] = useState(0);

  const hasStats = !!country?.laws || !!country?.cases || !!country?.policies;
  const hasEvents = !!country?.events && country?.events?.length > 0;
  const hasTargets = !!country?.targets && country?.targets?.length > 0;
  const hasDocuments = !!country?.documents && country?.documents?.length > 0;

  const documentCategories = DOCUMENT_CATEGORIES;
  const TARGETS_SHOW = 5;

  const handleDocumentCategoryClick = (e: any) => {
    return false;
  };
  const handleSortClick = (e: any) => {
    return false;
  };

  useEffect(() => {
    if (router.query.countryId) {
      refetch();
    }
  }, [router.query.countryId, refetch]);

  let targets = [];
  if (!!country?.targets) targets = showAllTargets ? country.targets : country.targets.slice(0, TARGETS_SHOW);

  if (isFetching) return <Loading />;

  return (
    <>
      <Layout title={`Climate Policy Radar | ${country?.name ?? "Loading..."}`}>
        {isError || !country ? (
          <SingleCol>
            <p>We were not able to load the data for the country.</p>
          </SingleCol>
        ) : (
          <section className="mb-8">
            <CountryHeader country={country} />
            <SingleCol>
              {hasStats && (
                <section className="grid grid-cols-2 md:grid-cols-3 gap-px rounded mb-8">
                  {!!country.laws && <KeyDetail detail="Laws" amount={country.laws} icon={<LawIcon />} />}
                  {!!country.policies && <KeyDetail detail="Policies" amount={country.policies} icon={<PolicyIcon />} />}
                  {!!country.cases && <KeyDetail detail="Cases" amount={country.cases} icon={<CaseIcon />} />}
                </section>
              )}
              {country.legislative_process && (
                <>
                  <h3 className="mb-4">Legislative Process</h3>
                  <div dangerouslySetInnerHTML={{ __html: country.legislative_process }} />
                </>
              )}
              {hasEvents && (
                <section className="mt-12">
                  <h3 className="mb-4">Events</h3>
                  <Timeline>
                    {country.events.map((event: TEvent, index: number) => (
                      <Event event={event} key={`event-${index}`} index={index} last={index === country.events.length - 1 ? true : false} />
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
                      Targets ({country.targets.length})
                    </h3>
                    <Targets targets={targets} />
                  </div>
                </section>
              )}
              {!showAllTargets && country?.targets?.length > TARGETS_SHOW && (
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
                    {country.documents.map((doc) => (
                      <div key={doc.related_id} className="mt-4 mb-10">
                        <RelatedDocument document={doc} />
                      </div>
                    ))}
                  </section>
                  <div className="mt-12">
                    <Divider>
                      <Link href="/search">
                        <Button color="secondary" extraClasses="flex items-center">
                          See more
                          <span className="ml-8">
                            <RightArrowIcon height="20" width="20" />
                          </span>
                        </Button>
                      </Link>
                    </Divider>
                  </div>
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
