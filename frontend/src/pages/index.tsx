import Link from 'next/link';
import Button from '../components/Button';
import Layout from '../components/Layout';
import axios from 'axios';

const IndexPage = () => {
  const postData = async (req: string): Promise<any> => {
    return await axios.post(req).then((response) => {
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
  };

  const submitForm = async (e) => {
    e.preventDefault();
    let req = 'http://localhost:8000/api/policies';
    return await postData(req);
  };
  return (
    <Layout title="Home | Submit new policy">
      <section>
        <div className="container py-4">
          <form>
            <h1>Submit new action</h1>
            <div className="my-4 flex">
              <label className="w-1/4">Name</label>
              <input className="ml-4 w-3/4" type="text" name="name" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Description</label>
              <textarea className="ml-4 w-3/4" name="description" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Year</label>
              <input className="ml-4 w-3/4" type="number" name="year" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Month</label>
              <input className="ml-4 w-3/4" type="number" name="month" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Day</label>
              <input className="ml-4 w-3/4" type="number" name="day" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Geography</label>
              <input className="ml-4 w-3/4" type="text" name="geography" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Languages</label>
              <input className="ml-4 w-3/4" type="text" name="languages" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Action type</label>
              <input className="ml-4 w-3/4" type="text" name="geography" />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Documents</label>
              <input
                className="ml-4 w-3/4"
                type="file"
                name="documents"
                multiple
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Document URLs</label>
              <input className="ml-4 w-3/4" type="text" name="url" />
            </div>
            <div className="my-4 flex">
              <Button onClick={submitForm}>Submit</Button>
            </div>
          </form>
        </div>
      </section>
    </Layout>
  );
};

export default IndexPage;
