import Layout from '../components/layouts/FullPageBanner';
import Dashboard from '../components/Dashboard';
import SearchInput from '../components/form-inputs/SearchInput';

const IndexPage = () => {
  return (
    <Layout
      title="Home | Law and Policy Search"
      heading="Law and Policy Search"
    >
      <div className="absolute top-0 left-0 w-full z-10 mt-52 md:mt-44 ">
        <div className="container py-4 overflow-x-hidden">
          <Dashboard />
          <SearchInput />
        </div>
      </div>
    </Layout>
  );
};

export default IndexPage;
