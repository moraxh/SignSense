// @ts-check
import { defineConfig, envField } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import icon from 'astro-icon';

export default defineConfig({
  vite: {
    server: {
        watch: { usePolling: true }
    },
    preview: {
      allowedHosts: true,
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