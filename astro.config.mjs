// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const base = '/feifeirong.github.io';

export default defineConfig({
  site: 'https://joanna910225.github.io',
  base,
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'zh'],
    routing: { prefixDefaultLocale: false },
  },
  redirects: {
    '/en': `${base}/`,
    '/en/about': `${base}/about`,
    '/en/blog': `${base}/blog`,
    '/en/news': `${base}/news`,
    '/en/projects': `${base}/projects`,
  },
  integrations: [sitemap()],
});
