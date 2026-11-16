<p align="center">
  <img 
    alt="YDL Logo" 
    width="220"
    src="https://raw.githubusercontent.com/YoungAndDigitalLearning/ydl-front/refs/heads/master/images/YDL-Logo-35px.svg"
  >
</p>
<h1 align="center">Young & Digital Learning</h1>

<p align="center">
  <!-- Workflow GitHub Actions - Deployment -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://github.com/YoungAndDigitalLearning/ydl-api/actions/workflows/deploy-api-docs.yml">
    <img 
      alt="API documentation deployment workflow status"
      src="https://img.shields.io/github/actions/workflow/status/YoungAndDigitalLearning/ydl-api/deploy-api-docs.yml?branch=feature%2Flocal-demo&style=for-the-badge&logo=githubactions&label=API%20Docs%20Deploy"
    >
  </a>
  <!-- Workflow GitHub Actions - Deployment status -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://github.com/YoungAndDigitalLearning/younganddigitallearning.github.io/deployments">
  <img
    alt="GitHub Pages deployment status"
    src="https://img.shields.io/github/deployments/YoungAndDigitalLearning/ydl-api/github-pages?style=for-the-badge&logo=githubpages&label=GitHub%20Pages"
  >
  </a>
  </br>
  <!-- Website Online/Offline -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://younganddigitallearning.github.io/ydl-api/">
    <img
      alt="Public API documentation website availability" 
      src="https://img.shields.io/website?url=https%3A%2F%2Fyounganddigitallearning.github.io%2Fydl-api%2F&style=for-the-badge&logo=githubpages&label=API%20Docs&up_message=online&down_message=offline&up_color=brightgreen&down_color=red" 
    >
  </a>
  <!-- Website Uptime 7 days -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://stats.uptimerobot.com/VNKWLhxGJn"
  >
    <img 
      alt="Uptime Robot ratio (7 days)" 
      src="https://img.shields.io/uptimerobot/ratio/7/m785998392-130996da3bf7ff5d6c432fb2.svg?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiI+CiAgPGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KICAgIDxjaXJjbGUgY3g9IjI1NiIgY3k9IjI1NiIgcj0iMjU2IiBmaWxsPSIjMkE4QzAwIi8+CiAgICA8Y2lyY2xlIGN4PSIyNTYuNSIgY3k9IjI1Ni41IiByPSIxNDEuNSIgZmlsbD0iIzIwMjAxRiIgc3Ryb2tlPSIjRkZGRkZGIiBzdHJva2Utd2lkdGg9IjIwIi8+CiAgPC9nPgo8L3N2Zz4K"
    >
  </a>
  </br>
  <!-- GitHub - Last commit -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://github.com/YoungAndDigitalLearning/ydl-api/commits/feature/local-demo"
  >
    <img 
      alt="Latest commit on feature local-demo branch"
      src="https://img.shields.io/github/last-commit/YoungAndDigitalLearning/ydl-api/feature/local-demo?style=for-the-badge&logo=github&label=Last%20Commit"
    >
  </a>
  </br>
  <!-- Django -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://github.com/YoungAndDigitalLearning/ydl-api">
    <img 
      alt="Python Django backend"
      src="https://img.shields.io/badge/Python-Django-3776AB?style=for-the-badge&logo=python&logoColor=white"
    >
  </a>
  </br>
  <!-- GitHub License -->
  <a 
    target="_blank"
    rel="noopener noreferrer"
    href="https://github.com/YoungAndDigitalLearning/ydl-api/blob/master/LICENSE"
  >
    <img 
      alt="GitHub License" 
      src="https://img.shields.io/github/license/YoungAndDigitalLearning/ydl-api?style=for-the-badge"
    >
  </a>
</p>

<p align="center">
  <a target="_blank" rel="noopener noreferrer" href="https://younganddigitallearning.github.io/ydl-api/"><strong>Browse Archived OpenAPI Reference</strong></a>
  ·
  <a target="_blank" rel="noopener noreferrer" href="https://younganddigitallearning.github.io/ydl-api/openapi.json">Download OpenAPI JSON</a>
  ·
  <a target="_blank" rel="noopener noreferrer" href="https://younganddigitallearning.github.io/">Explore Interactive Demo</a>
</p>

> **Documentation only.** Static, read-only Swagger UI built from a local Django OpenAPI export. There is no public API server; live requests are disabled.

## Backend

The **YDL REST API** is the server-side component of Young & Digital Learning, originally developed with Python, Django, and Django REST Framework.

The backend provides endpoints for user authentication, course enrollment, announcements, forum discussions, quizzes, and learning resources. MariaDB is used for persistent relational data storage.

The legacy backend has been restored for local development using Docker Compose, with fictional demonstration data for testing and documentation.

### API Documentation

The original API contract is available as an [archived OpenAPI reference](https://younganddigitallearning.github.io/ydl-api/), rendered using Swagger UI.

The documentation is **read-only** and does not expose a live Django backend.

[Explore Swagger UI](https://younganddigitallearning.github.io/ydl-api/) · [Download OpenAPI JSON](https://younganddigitallearning.github.io/ydl-api/openapi.json)

## Backend Documentation

- [Backend Architecture and REST API](https://github.com/YoungAndDigitalLearning/ydl/wiki/Backend-and-REST-API)
- [Local Development](https://github.com/YoungAndDigitalLearning/ydl/wiki/Local-Development)
- [Historical Server Setup](https://github.com/YoungAndDigitalLearning/ydl/wiki/Historical-Server-Setup)
- [Complete Project Wiki](https://github.com/YoungAndDigitalLearning/ydl/wiki)

The restored backend, including the fictional `seed_demo`
management command, is maintained on the
`feature/local-demo` branch.

## Setup tutorial

[Setup](https://github.com/YoungAndDigitalLearning/ydl-front/blob/master/Setup.md)

## Links

Our organization: [YoungAndDigitalLearning](https://github.com/YoungAndDigitalLearning)

Homepage: [YoungAndDigitalLearning.github.io/ydl-front](https://YoungAndDigitalLearning.github.io/)

Wikipage: [wiki](https://github.com/YoungAndDigitalLearning/ydl/wiki)

## Tech Stack YDL

<a target="_blank" rel="noopener noreferrer" href="https://raw.githubusercontent.com/YoungAndDigitalLearning/ydl-front/master/images/stack_features.jpg">
<img alt="Tech stack" src="https://raw.githubusercontent.com/YoungAndDigitalLearning/ydl-front/master/images/stack_features.jpg">
</a>

View bigger image file: [Image Link](https://raw.githubusercontent.com/YoungAndDigitalLearning/ydl-front/master/images/stack_features.jpg)

## Modules

- [Main](https://github.com/YoungAndDigitalLearning/ydl)
  - [Frontend](https://github.com/YoungAndDigitalLearning/ydl-front)
  - [Backend](https://github.com/YoungAndDigitalLearning/ydl-api)

---

Other Names:
YD Learning, Y&D Learning, Young & Digital Learning
