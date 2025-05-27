import type { NextApiRequest, NextApiResponse } from 'next';
import { ENV } from './env';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
     console.log(req.body);
    const searchParams = new URLSearchParams(req.body);

    // console.log(searchParams);
     
    if(!searchParams.has('token')){
      return res.status(400).json({ error: 'Missing token' });
    }

    const token = searchParams.get('token');
    const query = `CLEAR GRAPH <${ENV.NAMED_GRAPH}>;CLEAR GRAPH <${ENV.NAMED_GRAPH}/ontology>;CLEAR GRAPH <${ENV.NAMED_GRAPH}/goldendataset_demo>;`;

    // console.log('✅ Token:', token);
    console.log('✅ Query:', query);

    const response = await fetch(ENV.ECCENCA_ENDPOINT_WRITE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': `Bearer ${token}`,
      },
      body: new URLSearchParams({ update: query as string }),
    });

    const data = await response.text();
    res.status(response.status).send(data);

  } catch (error) {
    console.error('❌ Error in /api/cmem/clear:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
