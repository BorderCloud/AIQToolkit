
import type { NextApiRequest, NextApiResponse } from 'next';
import { ENV } from './env';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).end('Method Not Allowed');
  }

  try {
     console.log(req.body);
    const searchParams = new URLSearchParams(req.body);

    if(!searchParams.has('token') || !searchParams.has('eventId')){
    return res.status(400).json({ error: 'Missing eventId or token' });
  }

    const token = searchParams.get('token');
    const eventId = searchParams.get('eventId');
    const deleteQuery = `
        DELETE WHERE {
            GRAPH <${ENV.NAMED_GRAPH}/goldendataset_demo> {
                <${eventId}> ?p ?o .
            }
        }
    `;

     console.log(deleteQuery);
    const response = await fetch(ENV.ECCENCA_ENDPOINT_WRITE, {
    method: 'POST',
    headers: {
     'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Bearer ${token}`
    },
      body: new URLSearchParams({ update: deleteQuery as string }),
  });

    const data = await response.text();
    res.status(response.status).send(data);

     console.log(data);
    } catch (error) {
    console.error('❌ Error in /api/cmem/delete:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
