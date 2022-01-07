import Link from 'next/link';
import Layout from '../components/Layout';
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
