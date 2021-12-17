import Link from 'next/link';
import Layout from '../components/Layout';

const IndexPage = () => {
  return (
    <Layout title="Home | Submit new policy">
      <section>
        <div className="container">
          <form>
            <div className="my-4 flex">
              <label>Title</label>
              <input type="text" name="title" />
            </div>
          </form>
        </div>
      </section>
    </Layout>
  );
};

export default IndexPage;
