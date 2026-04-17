<template>
  <div class="about-page">
    <!-- Header -->
    <div class="page-hero">
      <div class="hero-content">
        <div class="hero-text">
          <span class="hero-badge">About</span>
          <h1 class="hero-title">关于我</h1>
          <p class="hero-desc">了解更多关于博主的信息</p>
        </div>
      </div>
    </div>

    <!-- Profile Card -->
    <div class="profile-card">
      <div class="profile-left">
        <div class="avatar">
          <span class="avatar-text">徐</span>
        </div>
        <h2 class="profile-name">徐联杰</h2>
        <p class="profile-title">Python Developer</p>
        <div class="profile-links">
          <a href="https://github.com/SilenceIsNotAlwaysGold" target="_blank" class="profile-link">
            <span class="link-icon">G</span> GitHub
          </a>
          <!-- 邮箱已隐藏 -->
        </div>
      </div>
      <div class="profile-right">
        <h3 class="section-title">个人简介</h3>
        <p class="bio-text">
          Python 后端开发工程师，专注于 AI 安全、大模型应用与后端系统开发。
          目前就职于北京云起无垠科技有限公司，专注于 AI 安全产品开发。
        </p>
        <p class="bio-text">
          拥有丰富的 Django、Flask、FastAPI 项目经验，擅长 LLM/RAG 技术集成、
          Text2SQL 智能体开发、Dify 工作流编排等 AI 应用落地。同时具备 Go 语言开发能力和
          Docker 容器化部署经验。
        </p>
      </div>
    </div>

    <!-- Work Experience -->
    <div class="info-section">
      <h3 class="section-title">工作经历</h3>
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-company">北京云起无垠科技有限公司</span>
              <span class="timeline-date">2025.05 - 至今</span>
            </div>
            <p class="timeline-role">Python 开发工程师</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-company">亿达信息技术有限公司</span>
              <span class="timeline-date">2023.10 - 2025.04</span>
            </div>
            <p class="timeline-role">后端开发 / 项目管理 / Prompt 工程师</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-company">湖南大咖说网络科技有限公司</span>
              <span class="timeline-date">2022.04 - 2023.10</span>
            </div>
            <p class="timeline-role">Python 开发工程师</p>
          </div>
        </div>
        <div class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-content">
            <div class="timeline-header">
              <span class="timeline-company">长沙箐箐科技有限公司</span>
              <span class="timeline-date">2020.07 - 2022.03</span>
            </div>
            <p class="timeline-role">Python 开发工程师</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Education -->
    <div class="info-section">
      <h3 class="section-title">教育背景</h3>
      <div class="edu-item">
        <div class="edu-header">
          <span class="edu-school">哈尔滨理工大学</span>
          <span class="timeline-date">2016.09 - 2020.07</span>
        </div>
        <p class="edu-major">计算机科学与技术（应用技术） | 本科</p>
      </div>
    </div>

    <!-- Skills -->
    <div class="info-section">
      <h3 class="section-title">技能专长</h3>
      <div class="skill-grid">
        <div class="skill-group">
          <h4 class="skill-label">编程语言</h4>
          <div class="skill-pills">
            <span class="pill accent">Python</span><span class="pill accent">Go</span>
            <span class="pill accent">C</span>
          </div>
        </div>
        <div class="skill-group">
          <h4 class="skill-label">Web 框架</h4>
          <div class="skill-pills">
            <span class="pill">Django</span><span class="pill">Flask</span>
            <span class="pill">FastAPI</span><span class="pill">DRF</span>
          </div>
        </div>
        <div class="skill-group">
          <h4 class="skill-label">AI / LLM</h4>
          <div class="skill-pills">
            <span class="pill warm">Prompt Engineering</span><span class="pill warm">RAG</span>
            <span class="pill warm">Text2SQL</span><span class="pill warm">Dify</span>
          </div>
        </div>
        <div class="skill-group">
          <h4 class="skill-label">数据库</h4>
          <div class="skill-pills">
            <span class="pill warm">MySQL</span><span class="pill warm">MongoDB</span>
            <span class="pill warm">Redis</span>
          </div>
        </div>
        <div class="skill-group">
          <h4 class="skill-label">中间件 & 工具</h4>
          <div class="skill-pills">
            <span class="pill muted">Kafka</span><span class="pill muted">Celery</span>
            <span class="pill muted">Elasticsearch</span><span class="pill muted">gRPC</span>
          </div>
        </div>
        <div class="skill-group">
          <h4 class="skill-label">DevOps</h4>
          <div class="skill-pills">
            <span class="pill muted">Docker</span><span class="pill muted">Nginx</span>
            <span class="pill muted">Linux</span><span class="pill muted">Git</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Contact -->
    <div class="info-section">
      <h3 class="section-title">联系方式</h3>
      <div class="contact-row">
        <!-- 邮箱已隐藏 -->
        <div class="contact-item">
          <span class="contact-icon">#</span>
          <div>
            <span class="contact-label">位置</span>
            <span class="contact-value">北京</span>
          </div>
        </div>
        <a href="https://github.com/SilenceIsNotAlwaysGold" target="_blank" class="contact-item contact-link">
          <span class="contact-icon">G</span>
          <div>
            <span class="contact-label">GitHub</span>
            <span class="contact-value">SilenceIsNotAlwaysGold</span>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.about-page {
  max-width: 860px;
  margin: 0 auto;
  padding: 0 2rem 3rem;
}

/* Hero */
.page-hero { padding: 2.5rem 0 1.5rem; }

.hero-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 2rem;
}

.hero-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  background: rgba(236, 72, 153, 0.15);
  color: #ec4899;
  margin-bottom: 0.5rem;
}

.hero-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.hero-desc {
  margin: 0.3rem 0 0;
  font-size: 0.95rem;
  color: var(--text-tertiary);
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 1.5rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 5px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: var(--card-border);
}

.timeline-item {
  position: relative;
  padding-bottom: 1.25rem;
}

.timeline-item:last-child { padding-bottom: 0; }

.timeline-dot {
  position: absolute;
  left: -1.5rem;
  top: 6px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--accent-primary);
  border: 2px solid var(--card-bg);
  box-shadow: 0 0 0 2px var(--accent-primary);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.2rem;
}

.timeline-company {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.timeline-date {
  font-size: 0.78rem;
  color: var(--text-disabled);
  white-space: nowrap;
}

.timeline-role {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

/* Education */
.edu-item { padding: 0; }

.edu-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.2rem;
}

.edu-school {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-primary);
}

.edu-major {
  margin: 0;
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

/* Profile Card - Fallback */
.profile-card {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 2rem;
  padding: 2rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.profile-left { text-align: center; }

.avatar {
  width: 100px;
  height: 100px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  background: var(--accent-gradient);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-text {
  font-size: 2.5rem;
  font-weight: 800;
  color: #fff;
}

.profile-name {
  margin: 0 0 0.25rem;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-primary);
}

.profile-title {
  margin: 0 0 1rem;
  font-size: 0.85rem;
  color: var(--text-tertiary);
}

.profile-links { display: flex; flex-direction: column; gap: 0.4rem; }

.profile-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.82rem;
  transition: all 0.2s;
}

.profile-link:hover { border-color: var(--accent-primary); color: var(--accent-primary); }

.link-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  background: var(--bg-tertiary);
  font-size: 0.7rem;
  font-weight: 700;
}

.profile-right { display: flex; flex-direction: column; }

.section-title {
  margin: 0 0 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '';
  width: 3px;
  height: 1em;
  background: var(--accent-gradient);
  border-radius: 2px;
}

.bio-text {
  margin: 0 0 0.75rem;
  font-size: 0.9rem;
  color: var(--text-secondary);
  line-height: 1.7;
}

.bio-text.hint {
  font-size: 0.8rem;
  color: var(--text-disabled);
  font-style: italic;
  margin-top: 0.5rem;
}

/* Info Section */
.info-section {
  padding: 1.5rem 2rem;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

/* Skills */
.skill-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.skill-label {
  margin: 0 0 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.skill-pills { display: flex; flex-wrap: wrap; gap: 0.35rem; }

.pill {
  font-size: 0.75rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  background: rgba(129, 140, 248, 0.1);
  color: var(--accent-primary);
  font-weight: 500;
}

.pill.accent { background: rgba(16, 185, 129, 0.1); color: #10b981; }
.pill.warm { background: rgba(245, 158, 11, 0.1); color: #f59e0b; }
.pill.muted { background: var(--bg-tertiary); color: var(--text-tertiary); }

/* Contact */
.contact-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  transition: border-color 0.2s;
}

.contact-item:hover { border-color: var(--accent-primary); }

.contact-link {
  text-decoration: none;
  cursor: pointer;
}

.contact-icon {
  font-size: 0.85rem;
  font-weight: 700;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--bg-tertiary);
  color: var(--text-tertiary);
  flex-shrink: 0;
}

.contact-label {
  display: block;
  font-size: 0.72rem;
  color: var(--text-disabled);
  margin-bottom: 0.1rem;
}

.contact-value {
  font-size: 0.85rem;
  color: var(--text-primary);
  font-weight: 500;
}

/* Mobile */
@media (max-width: 768px) {
  .about-page { padding: 0 1rem 2rem; }
  .profile-card { grid-template-columns: 1fr; }
  .skill-grid { grid-template-columns: 1fr; }
  .timeline-header { flex-direction: column; align-items: flex-start; gap: 0.2rem; }
  .edu-header { flex-direction: column; align-items: flex-start; gap: 0.2rem; }
}
</style>
