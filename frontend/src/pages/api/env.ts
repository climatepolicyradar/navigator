import { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log(`Getting ENV with: ${process.env.THEME} | ${process.env.NEXT_PUBLIC_API_URL}`)
  res.status(200).json({
    env: {
      theme: process.env.THEME,
      api_url: process.env.NEXT_PUBLIC_API_URL,
    },
  });
}
