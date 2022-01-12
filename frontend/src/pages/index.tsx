import { useState, useEffect } from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';
import AddAction from '../components/forms/AddAction';
import { getAuth, getData } from '../api';

const IndexPage = () => {
  const [geographies, setGeographies] = useState([]);
  const [languages, setLanguages] = useState([]);
  const [actionTypes, setActionTypes] = useState([]);
  const [sources, setSources] = useState([]);

  const filterLanguages = (langs) => {
    return langs.filter((lang) => lang.part1_code !== null);
  };
  const authenticate = async () => {
    await getAuth();
    fetchAll();
  };
  const fetchAll = async () => {
    const [geos, langs, actionTypes, sources] = await Promise.all([
      getData('geographies'),
      getData('languages'),
      getData('action_types'),
      getData('sources'),
    ]);
    setGeographies(geos);
    setLanguages(langs);
    setActionTypes(actionTypes);
    setSources(sources);
  };
  useEffect(() => {
    authenticate();
    // fetchAll();
  }, []);
  return (
    <Layout title="Home | Submit new policy">
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
  );
};

export default IndexPage;
