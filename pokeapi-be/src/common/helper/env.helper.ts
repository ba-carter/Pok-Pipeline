import { resolve } from 'path';

export function getEnvPath(dest: string): string {
  const env: string | undefined = process.env.NODE_ENV;
  const filename: string = env ? `.env` : '.production.env';
  return resolve(`${dest}/${filename}`);
}
