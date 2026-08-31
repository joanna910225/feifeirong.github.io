const base = import.meta.env.BASE_URL.replace(/\/$/, '');

export const withBase = (path = '') => {
  const clean = path.replace(/^\/+|\/+$/g, '');
  const suffix = clean && !/\.[^/]+$/.test(clean) ? '/' : '';
  return `${base}/${clean}${suffix}`;
};

export const localePath = (locale: 'en' | 'zh', path = '') =>
  withBase(`${locale === 'zh' ? 'zh/' : ''}${path.replace(/^\/+|\/+$/g, '')}`);

export const formatDate = (date: Date, locale: 'en' | 'zh') =>
  new Intl.DateTimeFormat(locale === 'zh' ? 'zh-CN' : 'en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  }).format(date);
