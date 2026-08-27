export type ResumeLocale = 'en' | 'zh';

export const resume = {
  en: {
    name: 'Feifei Rong',
    headline: 'AI Engineer · Python · AI Coding & Cross-Stack Delivery · Workflow Orchestration',
    contact: 'feifei.rong2@gmail.com',
    linkedin: 'https://www.linkedin.com/in/feifei-rong/',
    summary: [
      'AI engineer experienced in taking features from customer and business requirements through prototyping, implementation, testing, deployment, and launch; Python is my strongest language.',
      'In my current role, I participate across the full delivery lifecycle and lead the initial design of a node-based AI video workflow while maintaining its workflow-node library and main platform application.',
      'I also design deployment architectures for media-processing services and productionize ComfyUI workflows across cloud GPU and bare-metal environments.',
      'I worked full-time in London and am comfortable with the communication style and broad ownership of small, international startup teams.'
    ],
    skills: [
      ['AI Coding & Cross-Stack Delivery', 'Claude Code · Codex · task breakdown · context organization · review · debugging · testing · integration · release validation'],
      ['Workflow & Service Integration', 'REST APIs · model APIs · third-party services · workflow nodes · dependency-driven orchestration (DAG) · file and media processing'],
      ['Python & Search', 'Python · Flask · vector retrieval · semantic search · crawlers · FFmpeg'],
      ['Deployment & Runtime', 'Docker / Cog · ComfyUI · Custom Nodes · RunPod · Replicate · AutoDL · AWS · Alibaba Cloud FC / OSS'],
      ['Frontend Prototyping', 'Hand-coded HTML / JavaScript interfaces for semantic-search demos']
    ],
    experience: [
      {
        company: '河出图（上海）智能科技有限公司 (Dynampix)',
        role: 'AI Engineer',
        period: 'Dec 2024 - Present · Shanghai, China',
        bullets: [
          'Participate across the full delivery lifecycle and lead the initial design of a node-based workflow for batch AI video production, connecting scripting, TTS, avatars, B-roll, captions, and video services.',
          'Maintain the workflow-node library and main platform application; use Claude Code / Codex for task breakdown, context organization, and most implementation work while owning review, debugging, testing, integration, and release validation.',
          'Own deployment architecture and platform selection for media-processing services, defining each module\'s deployment model, hosting platform, invocation method, and media-asset flow.',
          'Productionize ComfyUI workflows across RunPod, Replicate, AutoDL, bare-metal hosts, and AWS, resolving platform entrypoints, Custom Nodes, model assets, Python / CUDA dependencies, container startup, and runtime-efficiency issues.'
        ]
      },
      {
        company: 'FADEL',
        role: 'AI Consultant · Part-time / Remote',
        period: 'Nov 2021 - Jan 2025',
        bullets: [
          'After FADEL acquired Image Data Systems, continued maintaining Python video-retrieval services and multimedia pipelines and integrated researcher-delivered models into Python application PoCs.',
          'Built and maintained e-commerce image / video crawlers and ingested collected assets into an enterprise media platform.',
          'Collaborated in English across time zones with a computer-vision advisor and R&D team members based in Beirut and France.'
        ]
      },
      {
        company: 'Image Data Systems (UK) Ltd',
        role: 'AI Engineer',
        period: 'Jan 2018 - Oct 2021 · London, UK',
        bullets: [
          'Worked with a computer-vision advisor to integrate facial recognition, pose estimation, and image clustering into a Python visual-search platform.',
          'Joined customer meetings and requirements discovery for enterprise image and video search.',
          'Built Flask APIs and hand-coded HTML / JavaScript interfaces for vector-backed semantic-search demos and AI tooling PoCs; deployed related Python services as Dockerized microservices.'
        ]
      },
      {
        company: 'Earlier Experience',
        role: '',
        period: '',
        bullets: [
          'ChinaSoft International · Software Test Engineer · IoT / networking performance testing and Linux troubleshooting',
          'Zhejiang Yizhou Electronic Technology · Embedded Software Engineer · educational robotics prototyping'
        ]
      }
    ],
    education: [
      'University of Bristol · MSc, Robotics · 2016 - 2017',
      'University of Southampton · Postgraduate Diploma, Computer Software Engineering · 2013 - 2014',
      'Institute of Technology, Tallaght · BEng, Electrical & Electronics Engineering · 2012 - 2013',
      'Nanjing University of Technology · BEng, Electronic Information Engineering · 2009 - 2013'
    ]
  },
  zh: {
    name: '戎菲菲',
    headline: 'AI 工程师 · Python · AI Coding 跨栈交付 · 工作流编排',
    contact: 'feifei.rong2@gmail.com',
    linkedin: 'https://www.linkedin.com/in/feifei-rong/',
    summary: [
      '具备 AI 功能 0 到 1 交付经验，能从客户和业务需求、原型验证推进到实现、测试、部署和上线；Python 是最熟练的主语言。',
      '当前全流程参与节点式 AI 视频工作流交付，主导前期方案设计，并维护工作流节点库和平台主应用。',
      '同时负责媒体处理服务的部署架构和方案选型，以及 ComfyUI 工作流的多平台生产化。',
      '曾在伦敦全职工作，适应小型国际化创业团队的沟通方式和较宽职责边界。'
    ],
    skills: [
      ['AI Coding 与跨栈交付', 'Claude Code · Codex · 任务拆解 · 上下文组织 · 改动审查 · 调试 · 测试 · 集成与上线验证'],
      ['工作流与服务集成', 'REST API · 模型 API · 第三方服务 · 工作流节点 · 节点式任务编排（DAG）· 文件与媒体处理'],
      ['Python 与检索', 'Python · Flask · 向量检索 · 语义搜索 · 爬虫 · FFmpeg'],
      ['部署与运行', 'Docker / Cog · ComfyUI · Custom Nodes · RunPod · Replicate · AutoDL · AWS · 阿里云 FC / OSS'],
      ['前端原型', '手写 HTML / JavaScript 语义搜索 Demo']
    ],
    experience: [
      {
        company: '河出图（上海）智能科技有限公司（Dynampix）',
        role: 'AI 工程师',
        period: '2024.12 - 至今 · 上海',
        bullets: [
          '全流程参与节点式 AI 视频工作流交付，主导前期方案设计，将文案、TTS、数字人、B-roll、字幕和视频服务拆分为可组合节点。',
          '维护工作流节点库和平台主应用；使用 Claude Code / Codex 做任务拆解、上下文组织和大部分实现，负责审查、调试、测试、集成和上线验证。',
          '负责媒体处理服务的部署架构和方案选型，确定各模块的部署形态、承载平台、调用方式及媒体文件流转。',
          '将同一套 ComfyUI 工作流适配 RunPod、Replicate、AutoDL、裸机和 AWS，处理平台入口、Custom Nodes、模型资产、Python / CUDA 依赖、容器启动和运行效率问题。'
        ]
      },
      {
        company: 'FADEL',
        role: 'AI 项目顾问 · 兼职 / 远程',
        period: '2021.11 - 2025.01',
        bullets: [
          'FADEL 收购 Image Data Systems 后，继续维护 Python 视频检索服务和多媒体数据管道，并将研究员交付的定制模型接入 Python 应用 PoC。',
          '开发和维护电商网站图片 / 视频采集爬虫，将素材接入企业媒体平台。',
          '日常使用英语，与计算机视觉顾问及分布在贝鲁特和法国的研发团队成员跨时区协作。'
        ]
      },
      {
        company: 'Image Data Systems (UK) Ltd',
        role: 'AI 工程师',
        period: '2018.01 - 2021.10 · 伦敦',
        bullets: [
          '与计算机视觉顾问合作，将人脸识别、姿态估计和图像聚类接入 Python 视觉检索平台。',
          '参与客户拜访和需求梳理，发展企业图片与视频的 AI 搜索能力。',
          '使用 Flask、HTML / JavaScript 手写基于向量数据库的语义搜索 Demo；将相关 Python 服务 Docker 化并以微服务方式部署。'
        ]
      },
      {
        company: '早期经历',
        role: '',
        period: '',
        bullets: [
          '中软国际 · 软件测试工程师 · IoT / 网络产品性能测试与 Linux 问题定位',
          '浙江一舟电子科技 · 嵌入式软件工程师 · 教育机器人原型开发'
        ]
      }
    ],
    education: [
      '布里斯托大学 · MSc Robotics · 2016 - 2017',
      '南安普顿大学 · Postgraduate Diploma, Computer Software Engineering · 2013 - 2014',
      '塔拉赫理工学院 · BEng Electrical & Electronics Engineering · 2012 - 2013',
      '南京工业大学 · BEng Electronic Information Engineering · 2009 - 2013'
    ]
  }
} as const;
