import type { NextApiRequest, NextApiResponse } from 'next'

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch('http://etl:5000/trigger-etl', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ start_id: 1, end_id: 20 }),
    });
    
    if (!response.ok) {
      throw new Error(`ETL service responded with status: ${response.status}`);
    }
    
    const result = await response.json();
    
    res.status(200).json({ 
      success: true,
      message: 'ETL pipeline triggered successfully',
      data: result 
    });
  } catch (error) {
    console.error('Error triggering ETL:', error);
    res.status(500).json({ 
      success: false,
      message: 'Failed to trigger ETL pipeline',
      error: error 
    });
  }
}