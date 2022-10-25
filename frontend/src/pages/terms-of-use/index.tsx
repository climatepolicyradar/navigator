import Layout from "@components/layouts/Main";
import { ExternalLink } from "@components/ExternalLink";

const TermsOfUse = () => {
  return (
    <Layout title={`Terms of use`}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Climate Change Laws of the World: Terms of use</h1>
          <h3>1. Introduction</h3>
          <p>1.1 Welcome to the terms of use for the Climate Change Laws of the World Database ("CCLW Database").</p>
          <p>
            1.2 The CCLW Database is operated by The Grantham Research Institute on Climate Change and Environment, part of the London School of Economics and Political Science
            ("We" or "LSE"), in partnership with the Sabin Center for Climate Change Law at Columbia Law School.
          </p>
          <p>
            1.3 The CCLW Database covers climate change laws, policies and climate litigation cases globally. It builds on more than a decade of data collection by both the
            Grantham Research Institute and the Sabin Centre.
          </p>
          <h3>2. Using the CCLW database</h3>
          <p>
            2.1 We actively encourage and support the use of information from the CCLW Database for a wide range of purposes, including but not limited to academic and policy
            research, teaching, engagement and advocacy.
          </p>
          <p>
            2.2 LSE, its collaborators, licensors, or authorised contributors own the copyright, database right and all other intellectual property rights (whether registered or
            unregistered and anywhere in the world) in the selection, coordination, arrangement and enhancement of the CCLW Database, as well as in the content original to it.
          </p>
          <p>
            2.3 We are pleased to make the content of the CCLW Database available under the Creative Commons Attribution Non-Commercial licence{" "}
            <ExternalLink url="https://creativecommons.org/licenses/by-nc/4.0/legalcode">(CC BY-NC 4.0)</ExternalLink>.
          </p>
          <p>2.4 Under this Creative Commons licence: </p>
          <p>
            <span className="font-bold">You are free to:</span>
          </p>
          <p>2.4.1 share, copy and redistribute the CCLW Database material in any medium or format; and</p>
          <p>2.4.2 adapt, transform and build upon the material from the CCLW Database.</p>
          <p>
            <span className="font-bold">Please ensure that you:</span>
          </p>
          <p>
            2.4.3 credit the LSE and its partners on all materials, publications, products or services which incorporate or use the information from the CCLW Database using the
            following notice: "Climate Change Laws of the World Database, copyright of the Grantham Research Institute on Climate Change and the Environment, London School of
            Economics and Political Science and Sabin Center for Climate Change Law, Columbia University. Sourced from{" "}
            <ExternalLink url="https://climate-laws.org">climate-laws.org</ExternalLink> and made available under the Creative Commons CC BY-NC licence."
          </p>
          <p>
            2.4.4 comply with the other terms of the Creative Commons licence, which include, without limitation, providing a disclaimer notice, indicating if changes have been
            made to the material and retaining a copy of any modifications.
          </p>
          <p>
            <span className="font-bold">You must not:</span>
          </p>
          <p>2.4.5 use the material for commercial purposes without prior permission from the LSE.</p>
          <p>2.5 You acknowledge that you do not acquire any ownership rights by downloading copyright material from the CCLW Database.</p>
          <p>
            2.6 LSE reserves the right to provide specific licences for commercial use. If you wish to use, copy, redistribute, publish or exploit a substantial amount of the
            information from the CCLW Database for commercial purposes please contact <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink> to discuss this.
          </p>

          <h3>3. Disclaimer</h3>
          <p>
            3.1 LSE gives no warranty or assurance about the content of the CCLW Database. As the CCLW Database is under constant development its contents may be incorrect or
            out-of-date and are subject to change without notice. While LSE makes every effort to ensure that the content of the CCLW Database is accurate, LSE cannot accept
            liability for the accuracy of its content at any given point in time. Any reliance that you may place on the information on the CCLW Database is at your own risk.{" "}
          </p>
          <p>
            3.2 If you find any inaccurate information, please let us know by emailing <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink> and we will
            correct it, where we agree, as soon as practicable.
          </p>
          <p>
            <span className="font-bold">3.3 Our trade marks</span>
          </p>
          <p>
            3.4 "Grantham Research Institute on Climate Change and the Environment" and its associated logo are unregistered trade marks of LSE. The use of these trade marks is
            strictly prohibited unless you have our prior written permission.
          </p>
          <p>
            <span className="font-bold">4. General terms</span>
          </p>
          <p>
            4.1 For details of all other terms applicable to The Grantham Research Institute on Climate Change and the Environment website and its content please visit{" "}
            <ExternalLink url="https://www.climate-laws.org/terms-of-use#:~:text=Terms%20of%20use%20(lse.ac.uk)">Terms of use (lse.ac.uk)</ExternalLink>.
          </p>
        </div>
      </section>
    </Layout>
  );
};

export default TermsOfUse;
