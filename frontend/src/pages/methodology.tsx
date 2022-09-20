import { useTranslation } from "react-i18next";
import Layout from "../components/layouts/Main";

const Methodology = () => {
  const { t } = useTranslation(["common"]);

  return (
    <Layout title={`Climate Policy Radar | ${t("Methodology")}`}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Methodology</h1>

          <h2>About this page </h2>
          <p>
            Welcome to the methodology page for the <a href="https://climatepolicyradar.org" target="_blank">Climate Policy Radar</a> search tool, which makes it possible to find information from
            within the full text of a large corpus of climate law and policy documents using semantic search.{" "}
          </p>
          <p>
            This page provides information about the scope and structure of our database, our data collection methods and terminology, updates to the database and planned future
            developments.
          </p>
          <p>
            As we expand and evolve, this methodology document will evolve to reflect developments. All previous versions will be linked here (this is the first one, so no previous
            versions yet).
          </p>
          <p>
            Currently (May 2022), the single source for the documents, summaries and data in this corpus is the{" "}
            <a href="https://climate-laws.org/" target="_blank">Climate Change Laws of the World database</a> (CCLW) maintained by the{" "}
            <a href="https://www.lse.ac.uk/granthaminstitute/" target="_blank">Grantham Research Institute on Climate Change and the Environment</a> at the{" "}
            <a href="https://www.lse.ac.uk/" target="_blank">London School of Economics and Political Science</a>. For this reason, this methodology page is substantially influenced by the
            methodology for the <a href="https://climate-laws.org/methodology-legislation" target="_blank">CCLW database</a>; please refer to that document for a full account of the scope of this
            database, and the terminology used.
          </p>
          <h2>Scope</h2>
          <p>
            Our dataset comprises national-level law and policy documents which pertain directly to policy issues concerning climate change mitigation, adaptation, loss and damage
            or disaster risk management. Documents in the database must have full legal force, having passed through the legislature or through an executive decision-making body,
            and/or set out a current governmental policy objective or set of objectives.
          </p>
          <p>
            The corpus of law and policy documents covers all parties to the UN Framework Convention on Climate Change (UNFCCC) — 196 countries plus the European Union — as well as
            a number of territories which are not party to the UN or UNFCCC — namely Taiwan, Palestine and Western Sahara.
          </p>
          <ul>
            <li className="italic">
              <span className="font-semibold">Glimpse into the future:</span> we will expand the dataset to include documents from subnational jurisdictions, such as state-level
              legislation, and to documents with international scope such as international treaties and documents submitted to the UNFCCC, such as Nationally Determined
              Contributions.
            </li>
          </ul>
          <p>
            For more information about the scope of the documents currently included in our dataset, please refer to the 'Scope of documents included' section of the{" "}
            <a href="https://climate-laws.org/methodology-legislation" target="_blank">CCLW methodology</a>.
          </p>
          <h2>Language</h2>
          <p>Our dataset contains documents published in many different languages. Non-English documents are assigned English titles, summaries and attributes. </p>
          <p>
            Currently, your searches will return results from all titles and summaries (regardless of language) as well as from the full text of all English documents; they do not
            return results from the full text of non-English documents.{" "}
          </p>
          <ul>
            <li className="italic">
              <span className="font-semibold">Glimpse into the future:</span> we will enable search on the full text of other languages starting with French and Spanish.{" "}
            </li>
          </ul>
          <h2>Updates to the database</h2>
          <p>
            The database is continually monitored and updated by teams of experts at Climate Policy Radar and at the LSE Grantham Research Institute, in order to ensure accuracy
            and to reflect the latest developments in climate law and policy. These updates are drawn from official sources such as government websites and parliamentary records.
          </p>
          <ul>
            <li className="italic">
              <span className="font-semibold">Glimpse into the future:</span> Frequent updates are planned to incorporate new types of data — including subnational laws and
              policies and documents submitted to the UNFCCC — which will be collected from new sources, including a range of databases and aggregators.{" "}
            </li>
          </ul>
          <h2>Data structure</h2>
          <p>Each entry in the database represents a single document (such as a law or a policy). Each document is assigned a title, summary and attributes (see below). </p>
          <p>
            Some documents in the database are associated with one or more additional documents. Documents may be associated with each other in a number of different ways — for
            example, one document may be a translation of another document, or an amendment to a document.{" "}
          </p>
          <h2>Attributes</h2>
          <p>Documents in the database are assigned attributes in order to provide information about the contents of documents and to support searchability. </p>
          <p>
            The attributes listed currently draw largely on taxonomies used in CCLW. In some cases, they are mutually exclusive - for example, a document is classified as either
            legislative or executive - and in some cases they are not - for example, one document may be relevant to multiple sectors. Equally, not all attributes are assigned to
            all documents: some documents have no sector tags.
          </p>
          <p>Attributes are manually assigned, and apply to entire documents.</p>
          <ul>
            <li className="italic">
              <span className="font-semibold">Glimpse into the future:</span> attributes will be automatically assigned using machine learning models, and will apply to individual
              paragraphs and sentences within the text of documents.{" "}
            </li>
          </ul>
          <p>
            For a full list of attribute types and values, please see{" "}
            <a href="https://docs.google.com/spreadsheets/d/1e5b5PqBPoQx_XhLV9z8SQ0VJQ2HCt87esLnw7S6OrtM/edit#gid=0" target="_blank">our codebook</a>.
          </p>
          <div className="m-table">
            <div className="row heading">
              <div className="term">Term</div>
              <div className="def">Definition</div>
            </div>
            <div className="row">
              <div className="term">Jurisdiction</div>
              <div className="def">
                A document’s jurisdiction indicates where it was published. Jurisdictions include all parties to the UN Framework Convention on Climate Change (UNFCCC) — 196
                countries plus the European Union — as well as a number of territories which are not party to the UN or UNFCCC, namely Taiwan, Palestine and Western Sahara.
              </div>
            </div>
            <div className="row">
              <div className="term">Region</div>
              <div className="def">
                Jurisdictions are grouped into regions of the world, as defined by the <a href="https://datahelpdesk.worldbank.org/knowledgebase/articles/906519" target="_blank">World Bank</a>.{" "}
              </div>
            </div>
            <div className="row">
              <div className="term">Year</div>
              <div className="def">
                Refers to the year in which a document was first published. Note - this may not be year of the most recent update or amendment to a document.
              </div>
            </div>
            <div className="row">
              <div className="term">Legislative</div>
              <div className="def">
                Documents categorised as legislative are those which are published on the authority of a legislative body within a country’s government, such as a parliament or
                assembly.{" "}
              </div>
            </div>
            <div className="row">
              <div className="term">Executive</div>
              <div className="def">
                Documents categorised as executive are those which are published on the authority of an executive body within a country’s government, such as a president or a
                monarch.
              </div>
            </div>
            <div className="row">
              <div className="term">Document type</div>
              <div className="def">The different formats of documents, such as laws, policies, strategies, action plans and decrees.</div>
            </div>
            <div className="row">
              <div className="term">Topics</div>
              <div className="def">
                Documents are labelled based on how their content relates to the broad aspects of climate action defined as Mitigation, Adaptation, Disaster Risk Management and
                Loss &amp; Damage. For more information about these terms, please see the 'Responses' section of the{" "}
                <a href="https://climate-laws.org/methodology-legislation" target="_blank">CCLW methodology</a>.
              </div>
            </div>
            <div className="row">
              <div className="term">Instruments</div>
              <div className="def">
                Instruments indicate the specific interventions or measures - such as regulations and taxes - set out in documents. The taxonomy of instruments was developed by the{" "}
                <a href="https://climate-laws.org/" target="_blank">LSE Grantham Research Institute</a> (see{" "}
                <a href="https://www.lse.ac.uk/granthaminstitute/publication/national-laws-and-policies-on-climate-change-adaptation-a-global-review/" target="_blank">Nachmany et al. 2019</a>
                ).
              </div>
            </div>
            <div className="row">
              <div className="term">Sectors</div>
              <div className="def">
                Sectors indicate the broad areas of economic activity - such as transport or agriculture - to which the content of documents relates. The list of sectors was
                synthesised by the <a href="https://climate-laws.org/" target="_blank">LSE Grantham Research Institute</a> — for more information, please see the 'Sectors' section of the{" "}
                <a href="https://climate-laws.org/methodology-legislation" target="_blank">CCLW methodology</a>.
              </div>
            </div>
            <div className="row">
              <div className="term">Keywords</div>
              <div className="def">Free text keywords are used to reflect the broad themes in the content of each document.</div>
            </div>
          </div>
          <h2>Data limitations</h2>
          <p>The principal limitations to our dataset stem from our data collection and our data labelling process.</p>
          <p>
            Our dataset currently relies on direct access to the Climate Change Laws of the World database. Updates to the dataset are made manually, based on monitoring of
            developments in climate law and policy internationally. We are developing the capacity to more efficiently capture data from additional sources, including via scraping,
            in order to increase the pace and scope of the expansion of our dataset.
          </p>
          <p>
            We currently rely on data labelled manually by domain experts; this limits the pace at which it is possible for new data to be incorporated into our dataset. We are
            developing the capacity to automatically label data using machine learning models, to increase the efficiency, sophistication and thoroughness of our data labelling.
          </p>
          <h2>Natural language search</h2>
          <p>
          Natural language search allows you to find what you’re looking for without having to type out precise keywords. This is useful because often certain concepts are described in lots of different ways - like internal combustion engines, internal combustion engine vehicle, ICEV, fossil fuel car, and gasoline car all describe most of the cars you’ll find on today’s roads. With natural language search, you can use the terms you use and hear everyday because the tool will recognise them as related and relevant terms, meaning you get a much richer search experience as a result.
          </p>
          <p>
          We use a machine learning method called dense retrieval alongside a fuzzy string search to perform natural language search. You can find more details <a href="https://climatepolicyradar.org/latest/building-natural-language-search-for-climate-change-laws-and-policies" target="_blank" >in our blog post</a>.
          </p>
          <h3>Biases &amp; limitations</h3>
          <p>
          The <a href="https://huggingface.co/sentence-transformers/msmarco-distilbert-dot-v5" target="_blank">model</a> we use for dense retrieval inherits biases from both its base model, <a href="https://huggingface.co/distilbert-base-uncased#limitations-and-bias" target="_blank">DistilBERT</a>, and the search query dataset it was trained on, <a href="https://github.com/microsoft/MSMARCO-Passage-Ranking/" target="_blank">MSMARCO</a>. It’s trained on relatively short passages of text (average 60 words in length), so may struggle with longer queries. 
          </p>
          <p>
          At the moment we use a general purpose model that has been trained on English Wikipedia and <a href="https://arxiv.org/abs/1506.06724v1" target="_blank">BookCorpus</a>. This means it may misinterpret some climate- or policy-specific concepts, and is something that we look to improve in future.
          </p>
          <h2>Additions? Contributions?</h2>
          <p>
            We work collaboratively with our users to keep our database at a high standard. Should you encounter any errors or inaccuracies in the data, we encourage you to get in
            touch with us at support@climatepolicyradar.org.
          </p>
        </div>
      </section>
    </Layout>
  );
};
export default Methodology;
