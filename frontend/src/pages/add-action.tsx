import { useState, useEffect } from 'react';
import Layout from '../components/layouts/Main';
import AddAction from '../components/forms/AddAction';
import { getAuth, getData } from '../api';
import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';

const AddActionPage = () => {
  const [geographies, setGeographies] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [actionTypes, setActionTypes] = useState([]);
  const [sources, setSources] = useState([]);

  const { t, i18n, ready } = useTranslation('addAction');

  const filterLanguages = (langs) => {
    return langs.filter((lang) => lang.part1_code !== null);
  };
  const authenticate = async () => {
    console.log('authenticating');
    await getAuth();
    fetchAll();
  };
  const fetchAll = () => {
    Promise.all([
      getData('geographies'),
      getData('languages'),
      getData('action_types'),
      getData('sources'),
    ])
      .then((values) => {
        const [geos, langs, actionTypes, sources] = values;
        setGeographies(geos);
        setLanguages(langs);
        setActionTypes(actionTypes);
        setSources(sources);
      })
      .catch((err) => {
        console.log(err);
        authenticate();
      });
  };
  useEffect(() => {
    const token = window.localStorage.getItem('jwt');
    if (token) {
      fetchAll();
      return;
    }
    // for now automatically authenticate a user
    authenticate();
  }, []);

  return (
    <>
      {!ready ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Add Action')}`}
          heading={t('Add Action')}
        >
          <section>
            <div className="container py-4">
              <AddAction
                geographies={geographies}
                languages={languages}
                actionTypes={actionTypes}
                sources={sources}
              />
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};

export default AddActionPage;
