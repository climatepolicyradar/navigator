import { ExternalLink } from "@components/ExternalLink";

const Methodology = () => {
  return (
    <section>
      <div className="text-content px-4 container mb-12">
        <h1 className="my-8">Methodology</h1>
        <p>
          Climate Change Laws of the World is continuously updated by researchers from the Grantham Research Institute at LSE. This page provides more information about our
          methodology. Read about:
        </p>
        <ul>
          <li>
            <a href="#legislation">The methodology for legislation and policy</a>
          </li>
          <li>
            <a href="#litigation">The methodology for litigation cases</a>
          </li>
          <li>
            <ExternalLink url="https://app.climatepolicyradar.org/methodology">
              The methodology used by Climate Policy Radar to power the search functions used by the database
            </ExternalLink>
          </li>
        </ul>
        <h2 id="legislation">Methodology - Legislation</h2>
        <h4>Introduction</h4>
        <div className="italic">
          <p>This legislation methodology was last updated on June 26th, 2022.</p>
          <p>
            This page outlines the definitions, scope, and principles used to collect and categorise the legislation displayed in the Climate Change Laws of the World database.{" "}
          </p>
          <p>
            Climate Change Laws of the World also tracks climate change litigation. For details on the methodology used to collect and categorise litigation cases{" "}
            <a href="#litigation">click here</a>.
          </p>
        </div>
        <h4>Scope of documents included</h4>
        <p>
          This database covers all UNFCCC parties (196 countries plus the European Union), as well as a number of territories that are not UN or UNFCCC such as Taiwan, Palestine
          and Western Sahara.
        </p>
        <p>
          The database focuses exclusively on climate change related laws and policies. We define climate change-related laws broadly, as legal documents that address policy areas
          directly relevant to climate change mitigation, adaptation, loss and damage or disaster risk management. Typically, to be included in the database one or more aspects of
          a law or policy must be demonstrably motivated by climate change concerns. More specifically, we consider legal documents that establish rules and procedures related to
          reducing energy demand; promoting of low carbon energy supply; restricting the development of fossil fuel based infrastructure; promoting low-carbon buildings; carbon
          pricing; lower industry emissions; tackling deforestation and promoting sustainable land use; other mitigation efforts; climate-related research and development;
          low-carbon transport; enhancing adaptation capabilities; natural disaster risk management. In some instances, laws addressing disaster risk management and/or energy
          related matters may have been included in the database even where no explicit mention of climate change is made, given the close connection between these areas and
          climate change. Laws aimed at enhancing other areas of environmental action or environmental protection are not included in the database unless they include provisions
          with directly relevant impacts on climate change action, such as a reduction in GHG emissions, significant enhancement, or protection of carbon sinks, or expressly
          contribute to climate adaptation and resilience.
        </p>
        <p>
          The database includes both legislation and policy at the national and sectoral level only. At present, it excludes information about the policy response of sub-national
          governments. It also excludes international legislation, such as treaties. Documents submitted only to international organisations such as the UNFCCC are generally
          excluded unless they have been converted into specific legislation or formally adopted as executive policies. In most cases, this means that documents such as the
          Long-term Low Emissions Development Strategies and National Adaptation Plans submitted to UNFCCC registries are not included in the databases. Users are encouraged to
          consult the relevant UN websites where these documents may be relevant to their search. For EU member states, laws transposing EU Directives are in the process of being
          added to the database along with the relevant EU law since in many instances these may contain additional relevant provisions. Where possible these additional provisions
          have been noted in the description of the relevant law.
        </p>
        <p>
          Documents included in the database must have full legal force, having passed through the legislature or through an executive decision-making body, and/or set out a
          current governmental policy objective or set of policy objectives. To the best of our ability, we capture major amendments to legislation and update document summaries
          accordingly. Where information is available that laws that are outdated, either because they have been repealed, replaced, or reversed, or because they were in force for
          a limited time period, these documents may be removed from the database. In general precedence is given to the document with the highest possible status dealing with a
          given matter. In some instances, policies or regulations aimed at giving effect to legislation or regulation of a higher order (“parent legislation”), such as statutory
          instruments or other guidance adopted to provide detail on the implementation of an act of parliament, may be included in the database alongside their “parent
          legislation” where these provide a significantly more detailed picture.
        </p>
        <p>In addition to tracking legislation, CCLW also contains information summarising national level climate targets. See Annex I below for more information.</p>
        <h4>Definitions and categorisation</h4>
        <p>
          We assign a number of codes and categories to all records in the CCLW database to enhance the usability and searchability of the data. The system of codes and categories
          has evolved over time to remain in step with developments in climate governance, the growth of the dataset, and the needs of our user community. Codes and categories
          currently in use include:
        </p>
        <p>
          <span className="block font-bold">Legislation and Policy</span>
          On addition to the database, documents are categorised as legislation or policy, in accordance with whether they are enacted by the legislative or executive branch of
          government. Where the same body holds both legislative and executive power, a determination of whether a document constitutes a law or policy is made based on our best
          understanding of the country’s legal system.
        </p>
        <p>
          <span className="block font-bold">Document types</span>
          Documents are also classified by document type. Document types are determined with reference to a non-exhaustive list of options and may be classified according to their
          legal status, i.e. as a Constitution or a Decree Law, or, in the case of policy documents, by their content, i.e. as a strategy, a roadmap, or a government guidance note.
        </p>
        <p>
          <span className="block font-bold">Responses</span>
          Laws and policies are categorised according to the climate policy response(s) to which they are most relevant, whether mitigation, adaptation, loss and damage, or
          disaster risk management. Where appropriate, laws may be tagged as relevant to more than one policy response.
        </p>
        <ol>
          <li>
            Mitigation: Mitigation laws and policies refer to a legislative or executive disposition focused on curbing a country’s greenhouse gases emissions in one sector or
            more. Measures can be directly related to emissions reductions, such as laws establishing a national carbon budget or cap and trade system, or indirectly related, such
            as laws or policies establishing relevant institutions or providing additional funding for research and development into low carbon technologies. Laws and policies
            addressing forests and land use are included as long as they explicitly support climate change mitigation through activities that reduce emissions and increase carbon
            removals. General forest management and conservation laws are not included, even if they may have implicit consequences for climate change mitigation.
          </li>
          <li>
            Adaptation: Adaptation laws and policies are those which contain explicit provisions concerning climate change adaptation, i.e. the need for changes in the management
            of ecological, social or economic systems in response to the actual or expected impacts of climate change. A comprehensive review of adaptation laws and policies was
            conducted in 2018 and documents have been added since then in real time. It must be noted, however, that in many cases, climate change adaptation responses may be
            embedded in development policies, general planning policies, risk-reduction and disaster management policies, water policies, land use and forestry policies and health
            policies, which can make them difficult to identify.<a href="#DandC-i">[i]</a>
          </li>
          <li>
            Disaster Risk Management: Laws and policies governing countries’ approaches to disaster risk management (DRM) and disaster risk reduction (DRR) were first added to the
            database in 2019. A broad approach to assessing whether these documents fall within the scope of this study has been adopted, as laws and policies often target natural
            and human disasters in a holistic manner, making it harder to isolate climate-related adverse events. Nonetheless, in determining whether a disaster risk management law
            or policy falls within the scope of this study researchers will usually consider whether the document relates to the types of disasters that are expected to become more
            frequent due to climate change, such as hurricanes, typhoons, flooding, heatwaves, droughts, forest fires, or sea-level rise (this list is non-exhaustive). Given the
            way in which these policies were added to the database, in some cases they may constitute exceptions to the general rule that laws and policies must be explicitly
            "climate-motivated" to justify their inclusion.
          </li>
          <li>
            Loss and Damage: For the purposes of this study, we define loss and damage related laws and policies as those that explicitly seek either to reduce the risk of
            climate-related loss and damage by increasing resilience or those that provide compensation or other relief measures to support victims of climate-related loss and
            damage. The guiding definition of loss and damage includes both economic and non-economic losses that arise due to climate impacts that are made more frequent or more
            severe by anthropogenic greenhouse gas emissions. Policy measures may include national climate relief funds, risk transfer mechanisms, internal relocation arrangements,
            mainstreaming loss and damage across government department and ministries and social protection programmes and safety nets. Loss and damage is the most recent policy
            response area included in the database. Our current categorisation accounts for documents that explicitly mention the term "loss and damage" and is exhaustive for laws
            and policies that were passed from 2015 onward. Documents addressing loss and damage with regard to specific impacts, such as biodiversity loss or drought, but which do
            not use an explicit loss and damage framing, do not have the loss and damage tag.
          </li>
        </ol>
        <p>
          <span className="block font-bold">Frameworks</span>A number of laws or policies in the database have been categorised as “framework” documents. While there is no agreed
          definition of a “climate change framework law”, this term is applied with increasing frequency to a discrete class of laws which share some or all of the following
          characteristics:
        </p>
        <ol>
          <li>Set out the strategic of travel for national climate change policy;</li>
          <li>Are passed by the legislative branch of government;</li>
          <li>Contain national long-term and /or medium targets and/ or pathways for change;</li>
          <li>Set out institutional arrangements for climate governance at the national level;</li>
          <li>Are multi-sectoral in scope; and</li>
          <li>
            Involve mechanisms for transparency and/or accountability.<a href="#DandC-ii">[ii]</a>
          </li>
        </ol>
        <p>
          Legislative documents contained in the Climate Change Laws of the World database are tagged as "framework laws" where these characteristics apply. However, in the case of
          executive policies, the definition employed here is broader than that adopted in recent literature regarding climate change framework legislation. Examples range from
          overarching multi-sectoral action plans, which serve to provide a unifying basis for climate change action within a country, to documents a narrower focus which
          nonetheless establish a governance framework for a specific aspect of climate action such as a national low-carbon energy policy. Data users interested in this sub-set of
          climate laws are advised to review the sub-set of laws tagged as frameworks and to use their discretion to determine which of these laws may be most relevant to their
          subject of inquiry.
        </p>
        <p>Framework documents are tagged to indicate the policy response area(s) to which they relate, whether mitigation, adaptation or disaster risk management.</p>
        <p>
          <span className="block font-bold">Instruments</span>
          In order to facilitate a more nuanced understanding of the ways in which governments around the world seek to influence the drivers and impacts of climate change,
          documents in the database are assessed to determine the primary policy instruments or “tools” on which they rely. Instruments are categorised according to an adapted
          version of the classic Hood and Margetts NATO typology of instruments.<a href="#DandC-iii">[iii]</a> Documents are assessed to determine the most relevant area(s) of
          government activity to which they relate and then tagged with the specific types of instrument they employ to achieve their stated aims and objectives. The vast majority
          of documents in the database will relate to more than one area of government activity and rely on multiple instruments. See Annex II below for a full list of instruments
          currently in use.
        </p>
        <p>
          <span className="block font-bold">Sectors</span>
          Each document is assessed to determine the most relevant sector or sectors to which it relates. The following sectors are currently considered: Agriculture, Transport,
          Energy, Waste, Environment, Tourism, LULUCF, Industry, Buildings, Water, Health, the Public Sector, and Other. Where a document relates to multiple sectors or appears
          cross-cutting in intention, we assign the labels “economy-wide” and or “cross-cutting area”. In some instances, multi-sectoral documents may also be categorised as
          related to Disaster Risk Management (DRM), Adaptation, or Social Development. We also consider whether laws relate primarily to urban or rural sectors of the economy
          and/or to coastal zones. We currently only cover waste laws that explicitly mention methane, another greenhouse gas, or if they deal with waste-to-energy schemes.
        </p>
        <p>
          <span className="block font-bold">Keywords</span>
          Discretionary keywords may also be assigned to cases to enable data users to identify these more easily. We do not maintain a comprehensive list of keywords.
        </p>
        <p>
          <span className="block font-bold">Notes</span>
          <span className="block" id="DandC-i">
            [i] Nachmany M, Byrnes R, Surminski S, 2019, National laws and policies on climate change adaptation: a global review. London: GRI Policy Brief
          </span>
          <span className="block" id="DandC-ii">
            [ii] See further: Nachmany M et al. 2015, “The 2015 Global Climate Legislation Study: A Review of Climate Change Legislation in 99 Countries” London: Grantham Research
            Institute , Nash, S. , & Steurer, R. 2019. “Taking stock of Climate Change Acts in Europe: Living policy processes or symbolic gestures?” Climate Policy 3:1, World
            Bank, 2020. “World Bank Reference Guide to Climate Change Framework Legislation” EFI Insight-Governance. Washington, DC: World
          </span>
          <span className="block" id="DandC-iii">
            [iii] See Hood C and Margetts H, 2007, The Tools of Government in the Digital Age, London: Macmillan Education. Hood and Margetts four basic “resources” of government –
            Nodality, Authority, Treasure and Organization are loosely mapped to areas of government activity as Capacity Building (Nodality), Regulation (Authority), Incentives
            and Direct Investment (Treasure), and Governance and Planning (Organization). These adaptations were developed to enhance the searchability of the database and to
            enable observations of particular relevance to climate change practitioners.
          </span>
        </p>
        <h4>Data collection process</h4>
        <p>
          The Climate Change Laws of the World Database started life in 2010 as printed publication, comprising an overview of climate change laws and policies in just 16
          countries. Since then, it has expanded to include all countries in the present scope and has moved online to enable users to access relevant information as and when it
          becomes available.
        </p>
        <p>
          Since the database has moved online, updates to the data are collected in real time from official sources such as government websites, parliamentary records and court
          documents. Most entries contain a link to the actual text of the law or the filing and court decision. The efforts of the CCLW team are regularly supplemented by
          contributions from lawyers, scholars, policymakers and other colleagues from around the world who alert us to new data as it becomes available. Please follow{" "}
          <ExternalLink url="https://docs.google.com/forms/d/e/1FAIpQLSdBdX2mLzFdeP8sTd_K7dsv8oylX6EBQucR_HhiXYZm1GA6gg/viewform">this link</ExternalLink> if you wish to contribute
          or email us at <ExternalLink url="mailto:gri.cgl@lse.co.uk">gri.cgl@lse.ac.uk</ExternalLink>.
        </p>
        <h4>Principles and Limitations</h4>
        <p>
          In general, our approach has been to be inclusive and flexible with definitions, in order to allow for the different regulatory approaches and cultures amongst 200
          countries, as well as to recognise the elusive boundaries of climate change, which by its nature spans multiple sectors and issues. We have also chosen to include policy
          and strategy documents which do not pass stringent legal tests of being 'legally binding' as by omitting them would have not captured the country's policy response.
          Likewise, where climate change overlaps significantly with other issues, such as development or disaster risk management, we have attempted to include those laws and
          policies that will be relevant to both issues.
        </p>
        <p>
          We aim for the data collected through this resource to be as comprehensive and accurate as possible. However, there is no claim to have identified every relevant law or
          policy in the countries covered. Language limitations, levels of media coverage, and the specific expertise of our researchers and contributors may all result in
          information for certain countries being more comprehensive than others.
        </p>
        <p>
          Although GRI has developed rigorous internal protocols to guide the process of data collection, the categorisation of each document has been determined by individual
          members of the CCLW team and has not generally been subject checks for inter-coder reliability. The records in the database have been published in a wide variety of
          languages, and researchers frequently use automated translation software to understand the content of these records. The determination of whether a given law is in scope,
          as well as its categorisation in accordance with the definitions outlined above, may therefore be open to differing interpretations.
        </p>
        <p>
          Users should also be aware that as our system of codes and categories evolves to better meet the needs of our user community, new codes may be assigned to records already
          in the database based on document summaries rather than a full review of the original documents. In some instances, this may mean that our codes and categories do not
          tell the full picture.
        </p>
        <p>
          Finally, we acknowledge that our current focus on national level legislation may mean that the database does not capture the full detail of the climate change policy
          response in many countries, particularly those where a significant quantity of climate action is governed by decision-making at the sub-national level.
        </p>
        <p>We invite users to exercise their judgment when using the data, and any data sub-sets that serve their research and policy purposes.</p>
        <h4>Annex I: Targets methodology</h4>
        <p>
          This Annex provides outlines the definitions, scope, and principles used to collect and categorise the targets displayed in the Climate Change Laws of the World database.
          Data on targets was originally collected in 2018 following a review of the{" "}
          <ExternalLink url="https://unfccc.int/process-and-meetings/the-paris-agreement/nationally-determined-contributions-ndcs/nationally-determined-contributions-ndcs">
            Nationally Determined Contributions(NDCs)
          </ExternalLink>{" "}
          submitted by parties to the Paris Agreement and around 1,500 climate change laws and policies then available in the CCLW database. In some instances where the text of the
          law was unavailable press releases or other secondary source material regarding the nature of targets set may have been consulted. Data has since been updated as new laws
          are added to the database, and as amendments to existing laws take place however this process is ongoing and data for some countries may be incomplete. This data has been
          reviewed extensively during the first semester of 2022, but some information such as the target type and scope are still missing. In parallel, economy-wide targets
          included in the second round NDCs are now uploaded for each country.
        </p>
        <p>
          <span className="block font-bold">Scope</span>
          In addition to legislation and litigation, the database also tracks national climate targets, as long as these are quantifiable. For ease of comparison, the database
          tracks quantifiable targets identified in countries NDCs in addition to quantifiable targets which have been incorporated into domestic law and policy (see definitions
          above). Both mitigation and adaptation targets are included. Aspirational or non-measurable targets are not generally included.
        </p>
        <p>
          <span className="block font-bold">Sector</span>
          Upon addition to the database, targets are categorised by sector (see above). Targets are defined as “economy-wide” if they are communicated on a national level, without
          further detail on the specific sectors to which they apply.
        </p>
        <p>
          <span className="block font-bold">Target details</span>
          For all targets, a target year and base year are included if possible. Emissions reduction targets classified according to the following target types:
          <a href="#TM-i">[i]</a>
        </p>
        <ol>
          <li>Base year target</li>
          <li>Fixed-level target</li>
          <li>Base year intensity target</li>
          <li>Baseline scenario target</li>
          <li>Trajectory target</li>
        </ol>
        <p>
          <span className="block font-bold">Notes</span>
          <span className="block" id="DandC-i">
            [i] For definitions of each target type see Fransen T, Northrop E, Mogelgaard K and Levin K (2017){" "}
            <ExternalLink url="https://www.wri.org/publication/ndc-enhancement-by-2020">
              Enhancing NDCs by 2020: Achieving the Goals of the Paris Agreement. Working Paper
            </ExternalLink>
            . Washington, DC: World Resources Institute.
          </span>
        </p>
        <h4>Annex II: List of Instruments</h4>
        <p>
          <span className="block font-bold">Regulation</span>
        </p>
        <ul>
          <li>Standards, obligations and norms</li>
          <li>Disclosure obligations</li>
          <li>Moratoria & bans</li>
          <li>Zoning & spatial planning</li>
          <li>Other</li>
        </ul>
        <p>
          <span className="block font-bold">Economic</span>
        </p>
        <ul>
          <li>Subsidies</li>
          <li>Tax incentives</li>
          <li>Carbon pricing & emissions trading</li>
          <li>Insurance</li>
          <li>Climate finance tools</li>
          <li>Other</li>
        </ul>
        <p>
          <span className="block font-bold">Direct Investment</span>
        </p>
        <ul>
          <li>Provision of climate funds</li>
          <li>Nature based solutions and ecosystem restoration</li>
          <li>Provision of climate finance</li>
          <li>Green procurement</li>
          <li>Early warning systems</li>
          <li>Other</li>
        </ul>
        <p>
          <span className="block font-bold">Governance</span>
        </p>
        <ul>
          <li>Capacity building</li>
          <li>Institutional mandates</li>
          <li>Planning</li>
          <li>Processes, plans and strategies</li>
          <li>MRV</li>
          <li>Subnational and citizen participation</li>
          <li>International cooperation</li>
          <li>Other</li>
        </ul>
        <p>
          <span className="block font-bold">Information</span>
        </p>
        <ul>
          <li>Education, training and knowledge dissemination</li>
          <li>Research & Development, knowledge generation</li>
        </ul>
        {/* LITIGATION */}
        <h2 id="litigation">Methodology - Litigation</h2>
        <div className="italic">
          <p>This ligitation methodology was last updated on May 4th, 2021.</p>
          <p>
            This page outlines the definitions, scope, and principles used to collect and categorise the litigation cases displayed in the Climate Change Laws of the World
            database.
          </p>
          <p>
            Climate Change Laws of the World also tracks climate change legislation. For details on the methodology used to collect and categorise legislation{" "}
            <a href="#legislation">click here</a>.
          </p>
        </div>
        <h4>Scope</h4>
        <p>
          At present, the Climate Change Litigation of the World database features cases from over 40 countries, including the EU as a block. Cases brought before international or
          regional courts or tribunals that meet the criteria set out below are included. This dataset does not include cases from the United States, which are collected separately
          by the <ExternalLink url="http://climatecasechart.com/us-climate-change-litigation/">Sabin Center / Arnold & Porter Kaye Scholer database</ExternalLink>.
        </p>
        <p>
          To fall within the scope of the database, cases must satisfy two key criteria. Firstly, cases must generally be brought before judicial bodies (though in some exemplary
          instances matters brought before administrative or investigatory bodies are also included). Secondly, climate change law, policy or science must be a material issue of
          law or fact in the case. Cases that make only a passing reference to climate change, but do not address climate-relevant laws, policies, or actions in a meaningful way
          are not included.
        </p>
        <p>
          In general, cases that may have a direct impact on climate change, but do not explicitly raise climate issues, are also not included in the database. Examples of such
          cases may include challenges to government inaction on air pollution or challenges to the development of fossil fuel infrastructure on the basis of other types of harm to
          human health and/or the environment. The intent of the litigants with regard to the climate-related consequences of such cases is not considered during the assessment
          process. One exception to this rule is that the database now includes a number of cases brought before arbitral tribunals under the terms of bilateral and multilateral
          international investment agreements, commonly referred to as Investor-State Dispute Settlement (ISDS). In these cases, private investors domiciled outside a given country
          typically seek compensation from the host country’s national governments for losses incurred as a result of policy changes and regulatory measuresthat unlawfully affect
          their investment (for example, by rendering the relevant assets not exploitable altogether), thus impacting the investment’s overall profitability. While these cases
          rarely contain explicit mentions of climate change, they are often closely related to and may impact on climate action at the national level. Cases are therefore
          considered to be within the scope of the database insofar as they relate directly to the enactment or withdrawal of a domestic measure explicitly adopted to meet a
          country’s climate goals and objectives. Examples of ‘climate-justified’ policy measures at the heart of these cases could include the enactment of plans to phase out
          coal-fired power plants within the coming decades or the withdrawal of existing subsidies or other incentives to encourage investment in renewable energy. More
          information on these cases and their inclusion in the database can be found{" "}
          <ExternalLink url="https://www.lse.ac.uk/granthaminstitute/news/investor-state-dispute-settlement-as-a-new-avenue-for-climate-change-litigation/">here</ExternalLink>.
        </p>
        <h4>Categorisation</h4>
        <p>Prior to addition to the database, cases are categorised according to:</p>
        <ol>
          <li>Jurisdiction, including the court or tribunal before which the case was filed (where this information is available);</li>
          <li>The type of parties involved (typically NGOs, individual, corporations, or governments); </li>
          <li>The status of the case – e.g. whether the case is filed, on appeal, or concluded;</li>
          <li>
            Whether the case primarily relates to climate change mitigation, adaptation, disaster risk reduction or loss and damage (see{" "}
            <a href="#legislation">CCLW Legislation Methodology</a> for definitions);
          </li>
          <li>
            The sector(s) of the economy to which the case is most relevant (see <a href="#legislation">CCLW Legislation Methodology</a> for definitions); and
          </li>
          <li>
            The primary laws to which the litigation relates. Where these laws are included in the Climate Change Laws of the World Database, the information is cross-referenced.
          </li>
        </ol>
        <p>Discretionary keywords may also be assigned to cases to enable data users to identify these more easily. We do not maintain a comprehensive list of keywords.</p>
        <h4>Data collection process</h4>
        <p>
          Cases are identified on a rolling basis by the Sabin Center for Climate Change Law, working in partnership with researchers at the Grantham Institute for Climate Change
          Research. Common sources of information relied on by researchers include media reports, legal databases, court websites and newsletters, social media, academic articles
          and other online sources. We take a collaborative approach to data gathering and many cases have been reported through networks of plaintiffs and defendants, academics
          and researchers, or crowdsourced through other channels.
        </p>
        <p>
          For some specific types of litigation, data is collected in partnership with other institutions. The primary source of cases from Australia is the University of
          Melbourne, which maintains the{" "}
          <ExternalLink url="https://law.app.unimelb.edu.au/climate-change/index.php#overview">Australian Climate Change Litigation Database</ExternalLink>. The primary source of
          cases from the Asia-Pacific region is the Asia Development Bank.
        </p>
        <p>
          Data regarding ISDS cases is collected in partnership with Hasselt University, Centre for Government and Law, Faculty of Law. The primary source of cases is the UNCTAD
          Investment Policy Hub database, which collects over 1.000 existing ISDS cases worldwide. Another source of information is the ICSID database on its website. Full details
          of complaints, decisions, and arbitral awards in ISDS cases are not always made public, but original documents are included in the database where these have been
          identified.
        </p>
        <p>
          Once a case is identified, it is reviewed by researchers at the Sabin Center for Climate Change Law with relevant expertise in the field of environmental and climate
          change law. Researchers draft case summaries and categorise cases according to the categories described above prior to entry into the databases.
        </p>
        <h4>Data Limitations</h4>
        <p>
          The database has helped highlight and inform a global field of practice in climate change law, providing information on more than 400 cases in over 40 countries. While we
          have sought to identify as many cases as possible that may fall within the scope outlined above, the database is not exhaustive. Key limitations include language
          barriers, levels of media coverage, and public availability of court documents. As a result, coverage in some jurisdictions is more comprehensive than in others. This may
          contribute to the wide discrepancy in the numbers of climate cases identified in different jurisdictions, although the legal culture in different jurisdictions should
          also be considered a key factor. In some instances, cases which are identical in subject matter may also have been recorded in the database in one entry. Similarly, the
          fact that no climate litigation has yet been identified in a given jurisdiction should not be taken as a certain indication that no such litigation has been filed.
        </p>
        <p>
          At present, the categorisation of cases is limited in scope. For example, the term government is used to identify a wide range of governments and institutions and may
          refer to national or subnational governments, or to specific government entities such as banks or other institutions. To mitigate this limitation, we do our best to
          specify the name of the government entities implicated in the litigation.
        </p>
        <p>
          The definition of climate change litigation found in some academic and practitioner-oriented literature is broader than that used to determine whether a case falls within
          the scope of these databases. The criteria for inclusion set out above has been adopted to facilitate both the process of data collection and to emphasise the distinct
          nature and importance of cases where climate change is material to the outcome. Climate change touches on a vast range of law and policy issues in the fields of
          environment, energy, natural resources, land use, and securities and financial regulation, among others; these criteria provide meaningful limits on researchers’
          discretion to determine whether a case has climate relevance and help define climate litigation as a distinct field. While the dataset is sufficiently comprehensive and
          cross-cutting to provide wide-ranging insights, data-users should be aware that individual cases that meet these criteria may be missing and certain trends may not
          currently be captured in the database. Some cases in the database are identified with the support of pro-climate litigants and their allies, which may mean that these
          cases are captured in more detail than cases seeking to challenge climate action. Our data collection processes are subject to continual evolution and may in future be
          modified to include additional categories of cases or to better capture the volume of cases of a given type.
        </p>
      </div>
    </section>
  );
};
export default Methodology;
