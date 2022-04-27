import Layout from "../components/layouts/Main";
import LoaderOverlay from "../components/LoaderOverlay";
import useActions from "../hooks/useActions";
import './i18n';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../api/auth';

const Actions = () => {
    const { user } = useAuth();
    const actionsQuery = useActions('actions');
    const { data } = actionsQuery;
    const { t, i18n, ready } = useTranslation('actions');

    return (
        <>
      {!actionsQuery.isSuccess || !ready || !user ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Laws and Policies')}`}
          heading={t('Laws and Policies')}
        >
          <section>
            <div className="container py-4">
              {data.items.map((action, index) => (
                    <div key={index} className="my-4">
                      <p className="font-bold">{action.name}</p>
                      <p>{action.description}</p>
                    </div>
              ))}
            </div>
          </section>
        </Layout>
      )}
    </>
    )

};
export default Actions;
