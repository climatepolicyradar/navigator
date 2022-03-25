import NextAuth from 'next-auth';
import Providers from 'next-auth/providers';
import axios from 'axios';
import CredentialsProvider from 'next-auth/providers/credentials';

// export default NextAuth({
//   // Configure one or more authentication providers
//   providers: [
//     CredentialsProvider({
//       // The name to display on the sign in form (e.g. "Sign in with...")
//       name: 'Credentials',
//       // The credentials is used to generate a suitable form on the sign in page.
//       // You can specify whatever fields you are expecting to be submitted.
//       // e.g. domain, username, password, 2FA token, etc.
//       // You can pass any HTML attribute to the <input> tag through the object.
//       // credentials: {
//       //   username: { label: "Username", type: "text", placeholder: "jsmith" },
//       //   password: {  label: "Password", type: "password" }
//       // },
//       authorize: async (credentials) => {
//         const user = await axios.post(
//           'http://localhost:8000/api/token',
//           {
//             user: {
//               password: credentials.password,
//               username: credentials.email,
//             },
//           },
//           {
//             headers: {
//               accept: '*/*',
//               'Content-Type': 'application/json',
//             },
//           }
//         );

//         if (user) {
//           return user;
//         } else {
//           return null;
//         }
//       },
//     }),
//   ],
//   callbacks: {
//     async jwt({ token }) {
//       token.userRole = 'admin';
//       return token;
//     },
//   },
// });

const providers = [
  CredentialsProvider({
    name: 'Credentials',
    authorize: async (credentials) => {
      const user = await axios.post(
        'http://localhost:8000/api/token',
        // 'grant_type=&username=user%40navigator.com&password=password&scope=&client_id=test&client_secret=super_secret',

        {
          user: {
            password: credentials.password,
            username: credentials.email,
          },
        },
        {
          // headers: {
          //   accept: '*/*',
          //   'Content-Type': 'application/json',
          // },
          headers: {
            accept: 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      if (user) {
        return user;
      } else {
        return null;
      }
    },
  }),
];

const callbacks = {
  // Getting the JWT token from API response
  async jwt(token, user) {
    if (user) {
      token.accessToken = user.token;
    }

    return token;
  },

  async session(session, token) {
    session.accessToken = token.accessToken;
    return session;
  },
};

const pages = {
  signIn: '/auth/signin',
  error: '/auth/error',
};

const options = {
  providers,
  callbacks,
  pages,
};

export default (req, res) => NextAuth(req, res, options);
