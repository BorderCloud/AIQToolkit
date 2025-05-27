import type { NextApiRequest, NextApiResponse } from 'next';
import { ENV } from './env';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const params = new URLSearchParams({
    grant_type: "password",
    client_id: "cmemc",
    username: ENV.ECCENCA_OAUTH_USER,
    password: ENV.ECCENCA_OAUTH_PASSWORD
  });

  try {
    const response = await fetch(
      ENV.ECCENCA_ENDPOINT_TOKEN,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: params.toString(),
      },
    );

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch token' });
  }
}
