import { useQuery } from 'react-query';
import { ApiClient } from '../api/http-common';
import { fakePromise } from '../helpers';
import { initialSearchCriteria } from '../constants/searchCriteria';

export default function useSearch(id, obj = initialSearchCriteria) {
  console.log(obj);
  const client = new ApiClient(); // note: remove baseUrl argument when api is finally ready
  // const fake = async () => {
  //   // get dummy data with latency added
  //   const value = await client.get('testdata/searches.json', obj);
  //   return fakePromise(500, value);
  // };
  const getResults = async () => {
    console.log(obj);
    const results = await client.post(`/searches`, obj, config);
    return results;
  };

  const config = {
    headers: {
      accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };

  return useQuery(
    id,
    () => {
      return getResults();
    },
    // fake(),
    { refetchOnWindowFocus: false, refetchOnMount: false }
  );
}
