import { useMutation } from '@tanstack/react-query';

const triggerETL = async () => {
  const response = await fetch('/api/trigger-etl', {
    method: 'POST',
  });
  if (!response.ok) {
    throw new Error('Failed to trigger ETL');
  }
  return response.json();
};

export const useTriggerETL = () => {
  return useMutation(triggerETL, {
    onSuccess: () => {
      console.log('ETL triggered successfully');
    },
    onError: (error) => {
      console.error('Error triggering ETL:', error);
    },
  });
};