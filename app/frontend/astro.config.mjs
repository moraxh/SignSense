// @ts-check
import { defineConfig, envField } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import icon from 'astro-icon';

const allowedHostsEnv = process.env.ALLOWED_HOSTS || '';
const allowedHosts = allowedHostsEnv
  .split(',')
  .map(host => host.trim())
  .filter(Boolean);

export default defineConfig({
  vite: {
    server: {
        watch: { usePolling: true },
        allowedHosts: allowedHosts,
    },
    preview: {
      allowedHosts: allowedHosts,
    },
    plugins: [tailwindcss()],
  },
  integrations: [icon()],
  env: {
    schema: {
      BACKEND_URL: envField.string({ context: 'client', access: 'public', default: 'ws://localhost' }),
    }
  }
});