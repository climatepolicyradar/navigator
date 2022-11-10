import { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({
    env: {
      theme: process.env.THEME,
      api_url: process.env.API_URL,
    },
  });
}

res.status(200).json({
  env: {
    theme: "cclw",
    api_url: "http://localhost:8000/api/v1"
  }
});
