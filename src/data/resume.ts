export type ResumeLocale = 'en' | 'zh';

export const resume = {
  en: {
    name: 'Feifei Rong',
    headline: 'AI Engineer · Generative AI / AIGC Productization · AI Workflow Platforms',
    contact: 'feifei.rong2@gmail.com',
    linkedin: 'https://www.linkedin.com/in/feifei-rong/',
    summary: [
      'Software engineer since 2014, focused on AI application delivery and production integration since 2018; Python is my primary and strongest language.',
      'Experienced in deploying ComfyUI workflows, integrating GPU-backed services across cloud environments, and building reliable AI workflow systems.',
      'I work with model researchers to turn research outputs into reliable services, focusing on engineering integration, deployment, validation, and service reliability.',
      'Full-time work experience in London and extensive collaboration in English with UK and globally distributed teams.'
    ],
    skills: [
      ['Generative AI Delivery', 'ComfyUI deployment and workflow integration · Gradio PoCs and demos · SD / SDXL / Flux / ControlNet / LoRA workloads'],
      ['Backend & Workflow', 'Python · TypeScript / Node.js · Fastify · PostgreSQL · Django · Flask · REST APIs'],
      ['Cloud & Deployment', 'Docker · AWS (EC2 / Lambda / S3) · RunPod · Replicate · AutoDL · Bare Metal · Alibaba Cloud FC / OSS'],
      ['Vision & Media', 'OpenCV · FFmpeg · visual search · production integration of computer-vision and multimedia models']
    ],
    experience: [
      { company: 'Dynampix', role: 'AI Engineer', period: 'Dec 2024 – Present · Shanghai, China', bullets: ['Deploy Dockerized ComfyUI workflows and integrate GPU-backed workloads across multiple cloud and bare-metal environments.', 'Build modules for an AI short-video workflow platform, owning requirements analysis, task decomposition, code review, testing, integration, and production reliability.', 'Govern self-contained dependencies and validation gates; design checkpoint, task-reuse, and uncertain-result safeguards for paid media operations.', 'Maintain a unified local / remote FFmpeg runner and remote execution support, with layered timeouts, body-idle watchdogs, and structured contextual logging.'] },
      { company: 'FADEL', role: 'AI Consultant · Part-time / Remote', period: 'Nov 2021 – Jan 2025', bullets: ['Evaluated engineering options, prepared data and interfaces, and integrated researcher-developed models into full-stack AWS PoCs.', 'Maintained Python / Django / Docker / AWS image-and-video retrieval services and automated multimedia ingestion pipelines.', 'Advised an English-speaking R&D team on architecture, technical standards, mentoring, and cross-time-zone onboarding.'] },
      { company: 'Image Data Systems (UK) Ltd', role: 'AI Engineer', period: 'Jan 2018 – Oct 2021 · London, UK', bullets: ['Developed Python / Django retrieval services and multimedia ingestion pipelines for a B2B visual-search platform.', 'Integrated facial-recognition, pose-estimation, and image-clustering models into production workflows.', 'Led a containerized annotation-and-training tooling PoC and automated AWS AMI builds with Packer.'] },
      { company: 'Earlier Experience', role: '', period: '', bullets: ['ChinaSoft International · Software Test Engineer · IoT / networking performance testing and Linux troubleshooting', 'Zhejiang Yizhou Electronic Technology · Embedded Software Engineer · educational robotics prototyping'] }
    ],
    education: ['University of Bristol · MSc, Robotics · 2016 – 2017', 'University of Southampton · Postgraduate Diploma, Computer Software Engineering · 2013 – 2014', 'Institute of Technology, Tallaght · BEng, Electrical & Electronics Engineering · 2012 – 2013', 'Nanjing University of Technology · BEng, Electronic Information Engineering · 2009 – 2013']
  },
  zh: {
    name: '戎菲菲',
    headline: 'AI 工程师 · AIGC 生产化 · AI 工作流与多云推理服务集成',
    contact: 'feifei.rong2@gmail.com',
    linkedin: 'https://www.linkedin.com/in/feifei-rong/',
    summary: ['自 2014 年起从事软件工程交付，2018 年起聚焦 AI 应用与生产集成；Python 为精通主语言。', '擅长将图像生成、计算机视觉及多媒体处理能力接入后端系统，覆盖容器化部署、工作流编排、外部服务集成与长任务可靠性。', '具备 ComfyUI 工作流部署、AI 辅助工程交付和跨云推理服务接入经验，专注工程接入、部署、验证与生产可靠性，并与算法研究员协作完成模型能力交付。', '曾在伦敦全职工作，并长期使用英语与英国及全球团队跨时区协作。'],
    skills: [['AIGC 应用工程', 'ComfyUI 工作流部署与服务接入 · Gradio PoC / Demo · SD / SDXL / Flux / ControlNet / LoRA'], ['后端与工作流', 'Python · TypeScript / Node.js · Fastify · PostgreSQL · Django · Flask · REST API'], ['云与部署', 'Docker · AWS（EC2 / Lambda / S3）· RunPod · Replicate · AutoDL · 裸机 · 阿里云 FC / OSS'], ['视觉与媒体', 'OpenCV · FFmpeg · 视觉检索 · 计算机视觉与多媒体模型生产集成']],
    experience: [{ company: 'Dynampix', role: 'AI 工程师', period: '2024.12 – 至今 · 上海', bullets: ['负责 ComfyUI 图像工作流的 Docker 化与部署，在多种云平台和裸机环境完成生成工作负载部署或服务接入。', '参与 AI 短视频工作流平台核心模块交付，负责需求分析、任务拆解、代码审查、测试、集成和生产可靠性。', '建立自包含依赖治理与验收门禁，为付费媒体操作设计 checkpoint、任务复用及不确定结果防护。', '维护统一本地 / 远端 FFmpeg runner 与远端执行适配，完善分层超时、body-idle watchdog 和结构化上下文日志。'] }, { company: 'FADEL', role: 'AI 项目顾问 · 兼职 / 远程', period: '2021.11 – 2025.01', bullets: ['负责工程侧方案评估、数据准备、接口与前后处理，将研究员完成的模型集成至全栈 AWS PoC。', '维护 Python / Django / Docker / AWS 图像视频检索服务，并构建自动化多媒体数据管道。', '为全英文 R&D 团队提供架构评估、技术规范、工程师带教和跨时区入职支持。'] }, { company: 'Image Data Systems (UK) Ltd', role: 'AI 工程师', period: '2018.01 – 2021.10 · 伦敦', bullets: ['开发 Python / Django 检索后端与多媒体数据接入管道，支持 B2B 视觉搜索平台。', '将人脸识别、姿态估计和图像聚类模型接入生产工作流。', '主导 Docker 化标注及训练工具 PoC，并使用 Packer 自动化构建 AWS AMI。'] }, { company: '早期经历', role: '', period: '', bullets: ['中软国际 · 软件测试工程师 · IoT / 网络产品性能测试与 Linux 问题定位', '浙江一舟电子科技 · 嵌入式软件工程师 · 教育机器人原型开发'] }],
    education: ['布里斯托大学 · MSc Robotics · 2016 – 2017', '南安普顿大学 · Postgraduate Diploma, Computer Software Engineering · 2013 – 2014', '塔拉赫理工学院 · BEng Electrical & Electronics Engineering · 2012 – 2013', '南京工业大学 · BEng Electronic Information Engineering · 2009 – 2013']
  }
} as const;
