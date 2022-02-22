import Layout from '../components/layouts/FullPageBanner';
import Dashboard from '../components/Dashboard';
import SearchForm from '../components/forms/SearchForm';
// import i18n (needs to be bundled ;))
import './i18n';

const IndexPage = () => {
  return (
    <Layout
      title="Home | Law and Policy Search"
      heading="Law and Policy Search"
    >
      <div className="absolute top-0 left-0 w-full z-10 mt-52 md:mt-44 ">
        <div className="container py-4 overflow-x-hidden">
          <Dashboard />
          <SearchForm />
        </div>
      </div>
    </Layout>
  );
};

export default IndexPage;
