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
