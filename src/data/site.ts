export const localePath = (locale: 'en' | 'zh', path = '') => {
  const clean = path.replace(/^\//, '');
  return locale === 'en' ? `/en${clean ? `/${clean}` : ''}` : `/zh${clean ? `/${clean}` : ''}`;
};

export const formatDate = (date: Date, locale: 'en' | 'zh') =>
  new Intl.DateTimeFormat(locale === 'zh' ? 'zh-CN' : 'en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
  }).format(date);
