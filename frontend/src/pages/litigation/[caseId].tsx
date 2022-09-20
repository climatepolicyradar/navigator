import { useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import Layout from "@components/layouts/Main";
import { CountryLink } from "@components/CountryLink";
import DocumentInfo from "@components/blocks/DocumentInfo";
import { AccordianItem } from "@components/accordian/AccordianItem";

const LitigationCoverPage = () => {
  const router = useRouter();
  const [showFullSummary, setShowFullSummary] = useState(false);
  console.log("Law id: ", router.query.caseId);

  const UNFCCCPillars = [
    {
      name: "Pillar",
    },
    {
      name: "P2",
    },
  ];
  const SECTORS = [
    {
      name: "Business",
    },
    {
      name: "Trade",
    },
  ];
  const KEYWORDS = [
    {
      name: "Keyword 1",
    },
    {
      name: "Keyword 2",
    },
  ];

  return (
    <Layout title={`Climate Policy Radar | Case title ${router.query.caseId}`}>
      <div className="mb-8">
        <div className="bg-offwhite border-solid border-blue-200 border-b">
          <div className="container">
            <div className="flex flex-col md:flex-row">
              <div className="flex-1 mt-6">
                <h1 className="text-3xl lg:smaller">Case title goes here vs. the opponent with a long title goes here</h1>
                <div className="flex text-base text-blue-700 mt-3 items-center w-full mb-2">
                  <CountryLink countryCode={"NLD"}>
                    <span className={`rounded-sm border border-black flag-icon-background flag-icon-nld`} />
                    <span className="ml-2">Netherlands</span>
                  </CountryLink>
                  <div className="ml-8">
                    <span className="font-bold mr-2">Filed</span> 14/09/2022
                  </div>
                  <div className="ml-8">Open</div>
                </div>
                <div className="flex text-sm text-blue-700 mt-3 items-center w-full mb-6">
                  <span className="font-bold mr-2">Reference</span> 12345678910
                </div>
              </div>
              <div className="hidden lg:block my-6 md:w-2/5 lg:w-1/4 md:pl-16 flex-shrink-0">&nbsp;</div>
            </div>
          </div>
        </div>
        <div className="container">
          <div className="md:flex">
            <div className="flex-1 md:w-0">
              <section className="mt-6 text-content">
                <h3 className="text-blue-700">Objectives</h3>
                <div
                  dangerouslySetInnerHTML={{
                    __html:
                      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut ullamcorper lacinia felis ut tincidunt. Curabitur in porta quam, nec ullamcorper ex. Quisque quis risus vitae lorem feugiat facilisis. Sed nec molestie metus, blandit facilisis est. Aenean sed nulla leo. Ut a odio ut libero hendrerit commodo in nec libero. Maecenas tempus molestie nulla ut convallis. In consequat purus sed elementum ultrices. Sed sit amet ultricies ex, quis lobortis felis. Phasellus mattis lacus ante, nec viverra lorem luctus id. ",
                  }}
                />
              </section>
              <section className="mt-12 text-content">
                <h3 className="text-blue-700">Summary</h3>
                <div
                  dangerouslySetInnerHTML={{
                    __html:
                      "Maecenas ac lectus eu justo accumsan placerat id vitae massa. Curabitur consectetur eget felis non viverra. Morbi ac nunc augue. Nullam sit amet purus sapien. Sed turpis arcu, ultricies eu pellentesque sed, eleifend et ex. Nullam vulputate eleifend sem. Fusce id maximus orci. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nullam et massa dapibus, mattis erat eget, sodales arcu. Vivamus eleifend quis mauris a iaculis. Sed interdum vulputate augue, in egestas enim vehicula eget. In eu luctus nisi. Aenean elementum nisi et enim posuere ultrices. Vivamus id turpis pulvinar, dictum massa vitae, interdum quam. Ut eleifend urna efficitur mauris commodo iaculis. Vestibulum varius leo eget elit lacinia, a hendrerit velit sodales.",
                  }}
                />
              </section>
              <section className="mt-12">
                <h3 className="text-blue-700">Events</h3>
                <div className="mt-2 mb-8">
                  <span className="py-1 px-3 bg-blue-600 text-sm font-bold text-white rounded-t">2022</span>
                  <AccordianItem
                    headerContent={
                      <>
                        <div className="flex-40">Summary of rejection</div>
                        <div>
                          by Court Name <span className="ml-4">12/09/2022</span>
                        </div>
                      </>
                    }
                  >
                    <div className="mt-4">
                      <p>
                        Maecenas ac lectus eu justo accumsan placerat id vitae massa. Curabitur consectetur eget felis non viverra. Morbi ac nunc augue. Nullam sit amet purus
                        sapien. Sed turpis arcu, ultricies eu pellentesque sed, eleifend et ex. Nullam vulputate eleifend sem. Fusce id maximus orci. Interdum et malesuada fames ac
                        ante ipsum primis in faucibus.
                      </p>
                      <p>
                        Nullam et massa dapibus, mattis erat eget, sodales arcu. Vivamus eleifend quis mauris a iaculis. Sed interdum vulputate augue, in egestas enim vehicula
                        eget. In eu luctus nisi. Aenean elementum nisi et enim posuere ultrices. Vivamus id turpis pulvinar, dictum massa vitae, interdum quam. Ut eleifend urna
                        efficitur mauris commodo iaculis. Vestibulum varius leo eget elit lacinia, a hendrerit velit sodales.
                      </p>
                      <ul>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                      </ul>
                    </div>
                  </AccordianItem>
                  <AccordianItem
                    headerContent={
                      <>
                        <div className="flex-40">Summary of rejection</div>
                        <div>
                          by Court Name <span className="ml-4">12/09/2022</span>
                        </div>
                      </>
                    }
                  >
                    <div className="mt-4">
                      <p>
                        Maecenas ac lectus eu justo accumsan placerat id vitae massa. Curabitur consectetur eget felis non viverra. Morbi ac nunc augue. Nullam sit amet purus
                        sapien. Sed turpis arcu, ultricies eu pellentesque sed, eleifend et ex. Nullam vulputate eleifend sem. Fusce id maximus orci. Interdum et malesuada fames ac
                        ante ipsum primis in faucibus.
                      </p>
                      <p>
                        Nullam et massa dapibus, mattis erat eget, sodales arcu. Vivamus eleifend quis mauris a iaculis. Sed interdum vulputate augue, in egestas enim vehicula
                        eget. In eu luctus nisi. Aenean elementum nisi et enim posuere ultrices. Vivamus id turpis pulvinar, dictum massa vitae, interdum quam. Ut eleifend urna
                        efficitur mauris commodo iaculis. Vestibulum varius leo eget elit lacinia, a hendrerit velit sodales.
                      </p>
                      <ul>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                      </ul>
                    </div>
                  </AccordianItem>
                </div>
                <div className="mt-2">
                  <span className="py-1 px-3 bg-blue-600 text-sm font-bold text-white rounded-t">2021</span>
                  <AccordianItem
                    headerContent={
                      <>
                        <div className="flex-40">Summary of rejection</div>
                        <div>
                          by Court Name <span className="ml-4">12/09/2022</span>
                        </div>
                      </>
                    }
                  >
                    <div className="mt-4">
                      <p>
                        Maecenas ac lectus eu justo accumsan placerat id vitae massa. Curabitur consectetur eget felis non viverra. Morbi ac nunc augue. Nullam sit amet purus
                        sapien. Sed turpis arcu, ultricies eu pellentesque sed, eleifend et ex. Nullam vulputate eleifend sem. Fusce id maximus orci. Interdum et malesuada fames ac
                        ante ipsum primis in faucibus.
                      </p>
                      <p>
                        Nullam et massa dapibus, mattis erat eget, sodales arcu. Vivamus eleifend quis mauris a iaculis. Sed interdum vulputate augue, in egestas enim vehicula
                        eget. In eu luctus nisi. Aenean elementum nisi et enim posuere ultrices. Vivamus id turpis pulvinar, dictum massa vitae, interdum quam. Ut eleifend urna
                        efficitur mauris commodo iaculis. Vestibulum varius leo eget elit lacinia, a hendrerit velit sodales.
                      </p>
                      <ul>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                      </ul>
                    </div>
                  </AccordianItem>
                  <AccordianItem
                    headerContent={
                      <>
                        <div className="flex-40">Summary of rejection</div>
                        <div>
                          by Court Name <span className="ml-4">12/09/2022</span>
                        </div>
                      </>
                    }
                  >
                    <div className="mt-4">
                      <p>
                        Maecenas ac lectus eu justo accumsan placerat id vitae massa. Curabitur consectetur eget felis non viverra. Morbi ac nunc augue. Nullam sit amet purus
                        sapien. Sed turpis arcu, ultricies eu pellentesque sed, eleifend et ex. Nullam vulputate eleifend sem. Fusce id maximus orci. Interdum et malesuada fames ac
                        ante ipsum primis in faucibus.
                      </p>
                      <p>
                        Nullam et massa dapibus, mattis erat eget, sodales arcu. Vivamus eleifend quis mauris a iaculis. Sed interdum vulputate augue, in egestas enim vehicula
                        eget. In eu luctus nisi. Aenean elementum nisi et enim posuere ultrices. Vivamus id turpis pulvinar, dictum massa vitae, interdum quam. Ut eleifend urna
                        efficitur mauris commodo iaculis. Vestibulum varius leo eget elit lacinia, a hendrerit velit sodales.
                      </p>
                      <ul>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                        <li>
                          <Link href="#">
                            <a className="underline text-blue-600">Document title often with long names</a>
                          </Link>
                        </li>
                      </ul>
                    </div>
                  </AccordianItem>
                </div>
              </section>
            </div>
            {/* Side */}
            <div className="mt-6 md:w-2/5 lg:w-1/4 md:pl-12 flex-shrink-0">
              <div className="md:pl-4 md:border-l md:border-blue-100">
                <section>
                  <h3 className="text-blue-700">About this case</h3>
                  <DocumentInfo id="court-tt" heading="Court / tribunal" text="Name of Court, Case field before" />
                  <DocumentInfo id="filed-tt" heading="Filed" text="File by, Party Type" />
                  <DocumentInfo id="responding-tt" heading="Responding" text="Responding party, Type" />
                  <DocumentInfo id="intervenor-tt" heading="Intervenor" text="Intervenor, Type" />
                  {1 > 0 && <DocumentInfo id="keywords-tt" heading="UNFCCC pillars" list={UNFCCCPillars} />}
                  {1 > 0 && <DocumentInfo id="sectors-tt" heading="Sectors" list={SECTORS} />}
                  {1 > 0 && <DocumentInfo id="keywords-tt" heading="Keywords" list={KEYWORDS} />}
                </section>
                <section className="mt-8 pt-4 border-t border-blue-100">
                  <h4 className="text-base text-indigo-400 font-semibold flex">Connected cases</h4>
                  <ul className="ml-4 list-disc list-outside mb-4">
                    <li>
                      <Link href="#">
                        <a className="underline text-blue-600">
                          Type of connection <br /> Case Title
                        </a>
                      </Link>
                    </li>
                    <li>
                      <Link href="#">
                        <a className="underline text-blue-600">
                          Type of connection <br /> Case Title
                        </a>
                      </Link>
                    </li>
                  </ul>
                  <h4 className="text-base text-indigo-400 font-semibold flex">Related laws</h4>
                  <ul className="ml-4 list-disc list-outside mb-4">
                    <li>
                      <Link href="#">
                        <a className="underline text-blue-600">Document name</a>
                      </Link>
                    </li>
                    <li>
                      <Link href="#">
                        <a className="underline text-blue-600">Document name</a>
                      </Link>
                    </li>
                  </ul>
                </section>

                <div className="mt-8 border-t border-blue-100">
                  <h3 className="text-blue-700 mt-4">Source</h3>
                  <div className="flex items-end mt-4">
                    <div className="relative flex-shrink max-w-[40px] mr-2">
                      <img src={`/images/partners/lse-logo.png`} alt="LSE logo" />
                    </div>
                    <p className="text-sm">Climate Change Laws of the World</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};
export default LitigationCoverPage;
