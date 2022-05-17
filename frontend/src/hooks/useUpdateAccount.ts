import { ApiClient } from '../api/http-common';
import { useMutation, useQueryClient } from 'react-query';

const useUpdateAccount = () => {
  const client = new ApiClient();
  const queryClient = useQueryClient();
  return useMutation((values) => client.put(`/users/me`, values), {
    onSuccess: (data: any) => {
      console.log(data);
      queryClient.setQueryData('auth-user', data.data);
    },
    onError: (err) => {
      console.log(err);
    },
    onSettled: () => {
      window.scrollTo(0, 0);
    },
  });
};

export default useUpdateAccount;

// curl -X 'PUT' \
//   'https://app.climatepolicyradar.org/api/v1/users/me' \
//   -H 'accept: application/json' \
//   -H 'Content-Type: application/json' \
//   -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXVsYSthdXRoX3Rlc3RfNTlAY2xpbWF0ZXBvbGljeXJhZGFyLm9yZyIsInBlcm1pc3Npb25zIjoidXNlciIsImlzX2FjdGl2ZSI6dHJ1ZSwiZXhwIjoxNjUyODAzMDM2fQ.4SGkQuHnVLJrOCLX8dTXLaEjEJL-tJXskwZXHZ_rhCM' \
//   -d '{
//   "names": "Paula H",
//   "job_role": "",
//   "location": "UK",
//   "affiliation_organisation": "x",
//   "affiliation_type": [
//     "string"
//   ],
//   "policy_type_of_interest": [
//     "string"
//   ],
//   "geographies_of_interest": [
//     "string"
//   ],
//   "data_focus_of_interest": [
//     "string"
//   ],
//   "email": "paula+auth_test_59@climatepolicyradar.org"
// }'
