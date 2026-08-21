import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    lang: z.enum(['en', 'zh']),
    category: z.string().optional(),
    tags: z.array(z.string()).default([]),
    description: z.string(),
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    lang: z.enum(['en', 'zh']),
    role: z.string(),
    period: z.string(),
    stack: z.array(z.string()).default([]),
    summary: z.string(),
    order: z.number().default(0),
    currentEmployer: z.boolean().default(false),
    status: z.string().optional(),
  }),
});

export const collections = { blog, projects };
