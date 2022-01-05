import Link from 'next/link';
import Button from '../components/Button';
import Layout from '../components/Layout';
import axios from 'axios';
import AddAction from '../components/forms/AddAction';

const IndexPage = () => {
  return (
    <Layout title="Home | Submit new policy">
      <section>
        <div className="container py-4">
          <AddAction />
        </div>
      </section>
    </Layout>
  );
};

export default IndexPage;
