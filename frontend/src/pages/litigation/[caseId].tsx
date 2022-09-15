import { useState } from "react";
import { useRouter } from "next/router";
import Layout from "@components/layouts/Main";
import { CountryLink } from "@components/CountryLink";

const LitigationCoverPage = () => {
  const router = useRouter();
  const [showFullSummary, setShowFullSummary] = useState(false);
  console.log("Law id: ", router.query.caseId);

  return (
    <Layout title={`Climate Policy Radar | Case title ${router.query.caseId}`}>
      <div className="mb-8">
        <div className="bg-offwhite border-solid border-blue-200 border-b">
          <div className="container">
            <div className="flex flex-col md:flex-row">
              <div className="flex-1 mt-6">
                <h1 className="text-3xl lg:smaller">Case title goes here vs. the opponent with a long title goes here</h1>
                <div className="flex text-sm text-blue-700 mt-3 items-center w-full mb-2">
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
              <div className="my-6 md:w-2/5 lg:w-1/4 md:pl-16 flex-shrink-0">
                Right side reserve
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};
export default LitigationCoverPage;
