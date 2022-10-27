import { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log("/api/env", process.env.NEXT_PUBLIC_THEME, process.env.NEXT_PUBLIC_API_URL);
  res.status(200).json({
    env: {
      theme: process.env.NEXT_PUBLIC_THEME,
      api_url: process.env.NEXT_PUBLIC_API_URL,
    },
  });
}
