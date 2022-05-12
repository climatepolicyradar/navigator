import { useAuth } from '../api/auth';
import Layout from '../components/layouts/Main';
import LoaderOverlay from '../components/LoaderOverlay';
import '../i18n';
import { useTranslation } from 'react-i18next';

const Terms = () => {
  const { user } = useAuth();
  const { t, i18n, ready } = useTranslation(['common']);
  return (
    <>
      {!user ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Navigator | ${t('Terms')}`}></Layout>
      )}
    </>
  );
};
export default Terms;
