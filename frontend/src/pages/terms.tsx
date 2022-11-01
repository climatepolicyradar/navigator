import { useTranslation } from "react-i18next";
import Layout from "../components/layouts/Main";

const Terms = () => {
  const { t } = useTranslation(["common"]);

  return (
    <Layout title={t("Terms")}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Terms of Use</h1>
          <h2>Introduction</h2>
          <p>
            Welcome to the terms of use for the Climate Policy Radar Database and Application ("CPR Database and App"). The CPR Database and App are operated by Climate Policy
            Radar CIC ("We" or "CPR"), and hosted at <a href="https://app.climatepolicyradar.org">https://app.climatepolicyradar.org</a>{" "}
          </p>
          <h2>Using the CPR Database and App under the CC-BY License </h2>
          <ul>
            <li>We actively encourage and support the use of information from the CPR Database and App for a wide range of purposes.</li>
            <li>
              CPR, its collaborators, licensors, or authorised contributors own the copyright, database right and all other intellectual property rights (whether registered or
              unregistered and anywhere in the world) in the selection, coordination, arrangement and enhancement of the CPR Database and App, as well as in the content original to
              it.
            </li>
            <li>
              We are pleased to make the content of the CPR Database available under the Creative Commons Attribution License 
              <a href="https://creativecommons.org/licenses/by/4.0/">(CC-BY)</a>.{" "}
            </li>
          </ul>
          <h2>Under this Creative Commons licence you are free to:</h2>
          <ul>
            <li>
              <span className="font-bold">Share — </span>copy and redistribute the CPR material in any medium or format
            </li>
            <li>
              <span className="font-bold">Adapt — </span>remix, transform, and build upon the material
            </li>
          </ul>
          <h2>License Terms:</h2>
          <p>We will not revoke these freedoms as long as you follow the license terms - see full legal code, which include but are not limited to these key issues:</p>
          <ul>
            <li>
              <span className="font-bold">Attribution — </span>You must give CPR <a href="https://creativecommons.org/licenses/by/4.0/#">appropriate credit</a>, provide a link to
              the license, and <a href="https://creativecommons.org/licenses/by/4.0/#">indicate if changes were made</a>. You may do so in any reasonable manner, but not in any way
              that suggests the licensor endorses you or your use. You may use this suggested text:
              <p>
                "Sourced from Climate Policy Radar, <a href="https://app.climatepolicyradar.org">https://app.climatepolicyradar.org</a> and made available under the Creative
                Commons CC BY licence."
              </p>
            </li>
            <li>
              <span className="font-bold">No additional restrictions — </span>
              You may not apply legal terms or <a href="https://creativecommons.org/licenses/by/4.0/#">technological measures</a> that legally restrict others from doing anything
              the license permits.
            </li>
            <li>
              <span className="font-bold">Exemptions and Limitations — </span>
              You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable{" "}
              <a href="https://creativecommons.org/licenses/by/4.0/#">exception or limitation</a>.
            </li>
            <li>
              <span className="font-bold">No warranties — </span>The license may not give you all of the permissions necessary for your intended use. For example, other rights such
              as <a href="https://creativecommons.org/licenses/by/4.0/#">publicity, privacy, or moral rights</a> may limit how you use the material.
            </li>
          </ul>
          <h2>Commercial Licensing</h2>
          <p>
            CPR reserves the right to provide specific licences for commercial use. If you wish to use, copy, redistribute, publish or exploit a substantial amount of the
            information from the CPR Database for commercial purposes please contact us by emailing support@climatepolicyradar.org to discuss this.{" "}
          </p>
          <h2>Disclaimer</h2>
          <ul>
            <li>
              Climate Policy Radar CIC gives no warranty or assurance about the content of the CPR Database. As the CPR Database is under constant development its contents may be
              incorrect or out-of-date and are subject to change without notice. While CPR makes every effort to ensure that the content of the CPR Database is accurate, CPR cannot
              accept liability for the accuracy of its content at any given point in time. Any reliance that you may place on the information on the CPR Database is at your own
              risk.
            </li>
            <li>
              If you find any inaccurate information please let us know by sending an email to support@climatepolicyradar.org and we will correct it, where we agree, as soon as
              practicable.
            </li>
          </ul>
          <h2>Our trade marks </h2>
          <p>
            "Climate Policy Radar” and its associated logo are unregistered trade marks of Climate Policy Radar CIC. The use of these trade marks is strictly prohibited unless you
            have our prior written permission.
          </p>
          <h2>Links To Other Sites</h2>
          <p>
            Our Database and App may contain links to third-party sites that are not owned or controlled by Climate Policy Radar. We have no control over, and assume no
            responsibility for, the content, privacy policies, or practices of any third party sites or services. We strongly advise you to read the terms and conditions and
            privacy policy of any third-party site that you visit.
          </p>
          <p>
            The CPR Database and App contains data that was created by third parties. Data that are sourced from third parties are clearly marked on the CPR Database and App. We
            strongly advise you to read the terms and conditions and privacy policy of any third-party data providers, noting they change from time to time.
          </p>
          <p>
            As of May 2022, the main source for third party data on the CPR Database and App is the Climate Change Laws of the World Database (”CCLW Database”) hosted by the
            Grantham Research Institute at the LSE. The Terms and Conditions governing the CCLW Database can be found here:{" "}
            <a href="https://climate-laws.org/terms-of-use">https://climate-laws.org/terms-of-use</a> and may change from time to time.{" "}
          </p>
          <h2>Changes To This Agreement</h2>
          <p>
            We reserve the right, at our sole discretion, to modify or replace these Terms and Conditions by posting the updated terms on the Site. Your continued use of the Site
            after any such changes constitutes your acceptance of the new Terms and Conditions.
          </p>
          <p>
            Please review this Agreement periodically for changes. If you do not agree to any of this Agreement or any changes to this Agreement, do not use, access or continue to
            access the Site or discontinue any use of the Site immediately.
          </p>
          <h2>Questions?</h2>
          <p>If you have any questions about this Agreement, please send an email to support@climatepolicyradar.org</p>
        </div>
      </section>
    </Layout>
  );
};
export default Terms;
