import { useRouter } from 'next/router';
import Layout from '../../components/layouts/Main';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import Loader from '../../components/Loader';
import Link from 'next/link';
import BackLink from '../../components/nav/BackLink';
import { truncateString } from '../../helpers';

const DocumentCoverPage = () => {
  const { t, i18n, ready } = useTranslation('searchStart');
  const summary =
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque turpis eros, tincidunt ac vulputate eget, mollis eu ligula. Cras in ex neque. Maecenas vel nibh condimentum, hendrerit enim vitae, tincidunt arcu. Ut tincidunt pellentesque ipsum sed fermentum. Vestibulum rutrum, tellus eu laoreet vehicula, leo risus pharetra enim, id tristique enim mauris ut enim. Nam varius suscipit augue, et maximus risus elementum at. Nulla facilisi. Nam convallis neque ut pretium bibendum. Aliquam id pulvinar eros. Curabitur volutpat vel ante sed finibus. Nulla vel elit lobortis, egestas augue sed, aliquet ligula. Donec auctor eu arcu a venenatis. Cras sit amet semper elit. Proin vel lorem sed ipsum ullamcorper interdum. Morbi at augue felis.';
  return (
    <Layout title={`Navigator | Document title`}>
      <div className="container mt-2"></div>
      <section>
        <div className="container">
          <BackLink href="/search" text="Back to search results" />
          <h1 className="mt-6 text-3xl font-medium">
            Energy Independence and Security Act of 2007
          </h1>
          <div className="flex text-xs text-indigo-400 mt-3">
            <div
              className={`rounded-sm border border-black flag-icon-background flag-icon-usa`}
            />
            <span className="ml-2">United States of America</span>
            <span className="ml-6">2009</span>
          </div>
          <div className="md:flex">
            <div className="flex-1">
              <div className="mt-6">{truncateString(summary, 250)}</div>
            </div>
            <div className="md:w-1/4 md:ml-8 flex-shrink-0">Right column</div>
          </div>
        </div>
      </section>
    </Layout>
  );
};
export default DocumentCoverPage;
