import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";
import Layout from "@components/layouts/Main";
import { ExternalLink } from "@components/ExternalLink";

const TermsOfUse = () => {
  const theme = useContext(ThemeContext);

  return (
    <Layout title={`Terms of use`}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Terms of use</h1>
          <h2>Introduction</h2>
          {theme === "cclw" && (
            <>
              <p>
                Welcome to Climate Change Laws of the World website, a leading resource on global climate law and policy. The website is offered through a partnership between the
                Grantham Research Institute at the London School of Economics and Climate Policy Radar.
              </p>
              <p>
                This website provides a user interface for the Climate Policy Radar Database and the Climate Policy Radar Application ("CPR Database and App"). The CPR Database
                builds on over a decade of work at the Grantham Research Institute to provide data and insights on climate change law and policy worldwide to support informed and
                ambitious climate change policymaking and research.
              </p>
            </>
          )}
          {theme === "cpr" && (
            <>
              <p>Welcome to Climate Policy Radar, a leading resource on global climate law and policy. </p>
              <p>
                This website provides a user interface for the Climate Policy Radar Database and the Climate Policy Radar Application ("CPR Database and App"). The CPR Database
                builds on over a decade of work at the Grantham Research Institute to provide data and insights on climate change law and policy worldwide to support informed and
                ambitious climate change policymaking and research. The work is underpinned by a partnership between the Grantham Research Institute at the London School of
                Economics and Climate Policy Radar.
              </p>
            </>
          )}
          <p>
            The following Terms govern the use of the CPR Database and App and the ‘Climate Change Laws of the World’ interface for the Climate Policy Radar App (”CCLW Interface”).
          </p>
          <p>
            The CPR Database and App are operated by <ExternalLink url="https://climatepolicyradar.org/">Climate Policy Radar CIC</ExternalLink> ("CPR"). The CCLW Interface is
            jointly operated by CPR and the Grantham Research Institute on Climate Change and the Environment at the London School of Economics (”GRI”), and hosted at{" "}
            <ExternalLink url="https://climate-laws.org/">https://climate-laws.org</ExternalLink>.
          </p>
          <p>
            To access the methodology and code book for the CPR Database and its third party data providers, please{" "}
            <ExternalLink url="https://github.com/climatepolicyradar/methodology">click here</ExternalLink>.
          </p>
          <h2>Using the CPR Database and App</h2>
          <ul>
            <li>
              Climate Policy Radar actively encourages and supports the use of information from the CPR Database and App {theme === "cclw" && <>via the CCLW Interface</>} for a
              wide range of purposes.
            </li>
            <li>
              Climate Policy Radar, its collaborators, licensors, or authorised contributors to the CPR Database and App own the copyright, database right and all other
              intellectual property rights (whether registered or unregistered and anywhere in the world) in the selection, coordination, arrangement and enhancement of the CPR
              Database and App, as well as in the content original to it.
            </li>
          </ul>
          <h3>Open data under the CC-BY Licence</h3>
          <ul>
            <li>
              Climate Policy Radar is pleased to make the content of the CPR Database available as open data under the Creative Commons Attribution Licence 
              <ExternalLink url="https://creativecommons.org/licenses/by/4.0/">(CC-BY)</ExternalLink>. Under this Creative Commons licence you are free to:
              <ul>
                <li>
                  <span className="font-bold">Adapt</span> — remix, transform, and build upon the material
                </li>
                <li>
                  <span className="font-bold">Share</span> — copy and redistribute the CPR material in any medium or format{" "}
                </li>
              </ul>
            </li>
            <li>
              <span className="font-bold">Licence terms</span>: Climate Policy Radar will not revoke these freedoms as long as you follow the license terms - see [full legal
              code](https://creativecommons.org/licenses/by/4.0/legalcode), which include but are not limited to these key issues:
              <ul>
                <li>
                  <span className="font-bold">Attribution</span>: You must give CPR and its partners [appropriate credit](https://creativecommons.org/licenses/by/4.0/#), provide a
                  link to the license, and [indicate if changes were made](https://creativecommons.org/licenses/by/4.0/#). You may do so in any reasonable manner, but not in any
                  way that suggests the licensor endorses you or your use. See suggested citation below.
                </li>
                <li>
                  <span className="font-bold">No additional restrictions</span>: You may not apply legal terms or [technological
                  measures](https://creativecommons.org/licenses/by/4.0/#) that legally restrict others from doing anything the license permits.
                </li>
                <li>
                  <span className="font-bold">Exemptions and Limitations</span>: You do not have to comply with the license for elements of the material in the public domain or
                  where your use is permitted by an applicable [exception or limitation](https://creativecommons.org/licenses/by/4.0/#).
                </li>
                <li>
                  <span className="font-bold">No warranties</span>: The license may not give you all of the permissions necessary for your intended use. For example, other rights
                  such as [publicity, privacy, or moral rights](https://creativecommons.org/licenses/by/4.0/#) may limit how you use the material.
                </li>
              </ul>
            </li>
          </ul>
          <h3>Recommended citation</h3>
          <ul>
            <li>
              <p>When citing use of the Database, you may use this text:</p>
              {theme === "cclw" && (
                <p className="italic">
                  "Sourced from ‘Climate Change Laws of the World’ interface for the Climate Policy Radar Database, https://climate-laws.org and made available under the Creative
                  Commons CC-BY licence. The data in this database was sourced primarily from the Grantham Research Institute at the London School of Economics.
                </p>
              )}
              {theme === "cpr" && (
                <p className="italic">
                  "Sourced from the Climate Policy Radar Database, https://app.climatepolicyradar.org and made available under the Creative Commons CC-BY licence. The data in this
                  database was sourced primarily from the Grantham Research Institute at the London School of Economics."
                </p>
              )}
            </li>

            <li>
              <p>When citing a specific data point(s), for example, if citing a summary of a document, please use the following citation:</p>
              {theme === "cclw" && (
                <p className="italic">
                  “This summary was written by researchers at the Grantham Research Institute at the London School of Economics, sourced from Climate Policy Radar via ‘Climate
                  Change Laws of the World’, https://climate-laws.org/ and made available under and under the Creative Commons CC-BY licence”.
                </p>
              )}
              {theme === "cpr" && (
                <p className="italic">
                  “This summary was written by researchers at the Grantham Research Institute at the London School of Economics, sourced from Climate Policy Radar,
                  https://app.climatepolicyradar.org and made available under and under the Creative Commons CC-BY licence”
                </p>
              )}
              <p>
                <span className="font-bold">Note</span>: As of November 2022, all summaries in the CPR App were written by researchers at the Grantham Research Institute (as
                reflected on every document page). This section and recommended citation will be updated to reflect any changes to this.
              </p>
            </li>
          </ul>
          <h2>Commercial Licensing</h2>
          <p>
            Climate Policy Radar reserves the right to provide specific licences for commercial use. If you wish to use, copy, redistribute, publish or exploit a substantial amount
            of the information from the CPR Database for commercial purposes please contact us by emailing support@climatepolicyradar.org to discuss this.
          </p>
          <h2>Disclaimer</h2>
          <ul>
            <li>
              Climate Policy Radar gives no warranty or assurance about the content of the CPR Database. As the CPR Database is under constant development its contents may be
              incorrect or out-of-date and are subject to change without notice. While Climate Policy Radar makes every effort to ensure that the content of the CPR Database is
              accurate, CPR cannot accept liability for the accuracy of its content at any given point in time. Any reliance that you may place on the information on the CPR
              Database is at your own risk.
            </li>
            <li>The content in the CPR database, including any third party data, does not constitute legal advice. No warranty of accuracy or completeness is made.</li>
            <li>
              If you identify incomplete or inaccurate information please let us know by <ExternalLink url="https://forms.gle/J1va24deERTSs8LXA">filling this form</ExternalLink>{" "}
              and Climate Policy Radar will endeavour to complete or correct it, as soon as practicable.
            </li>
          </ul>
          <h2>Our trade marks</h2>
          <p>
            "Climate Policy Radar” and its associated logo are unregistered trade marks of Climate Policy Radar CIC. The use of these trade marks is strictly prohibited unless you
            have our prior written permission.
          </p>
          <h2>Links to other sites</h2>
          <p>
            The CPR Database and App may contain links to third-party sites that are not owned or controlled by Climate Policy Radar. Climate Policy Radar has no control over, and
            assumes no responsibility for, the content, privacy policies, or practices of any third party sites or services. Climate Policy Radar strongly advises you to read the
            terms and conditions and privacy policy of any third-party site that you visit.
          </p>
          <h3>Data from Third Party Sources</h3>
          <p>
            The CPR Database and App contains data that were created by third parties. The data includes document summaries that were written by third parties and/or information
            about the documents (”meta-data”) assigned by third parties, e.g. classifications to sector or legal principle.
          </p>
          <p>
            Data that are sourced from third parties are clearly marked on the CPR Database and App. Climate Policy Radar strongly advises you to read the terms and conditions and
            privacy policy of any third-party data providers, noting they change from time to time. Below are listed data sources for third party data on the CPR Database and App:
          </p>
          <table className="text-left">
            <thead>
              <tr>
                <th>Source</th>
                <th>Data</th>
                <th>Date added</th>
                <th>Third party terms and conditions</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Grantham research Institute, LSE</td>
                <td>Law and policy document summaries; selected document metadata</td>
                <td>October 2022</td>
                <td>
                  <ExternalLink url="https://www.lse.ac.uk/granthaminstitute/cclw-terms-and-conditions">View</ExternalLink>
                </td>
              </tr>
              <tr>
                <td>Additional data sources will be added here as they are added to the CPR database and app</td>
                <td></td>
                <td></td>
                <td></td>
              </tr>
            </tbody>
          </table>
          <h2>Changes To This Agreement</h2>
          <p>
            Climate Policy Radar reserves the right, at our sole discretion, to modify or replace these Terms and Conditions by posting the updated terms on the Site. Your
            continued use of the Site after any such changes constitutes your acceptance of the new Terms and Conditions.
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

export default TermsOfUse;
