# Commission Intelligence Platform - Bootstrap Version

## Overview

This is the bootstrap version of the Commission Intelligence Platform, designed to run on a shoestring budget ($30-50/month) while looking like a million-dollar platform. Built specifically for the "sell first, build second" strategy.

## Quick Start

### 1. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd bootstrap_platform

# Start all services with Docker
docker-compose up -d

# Access the services:
# - Landing Page: http://localhost
# - API: http://localhost:8000
# - Admin Panel: http://localhost:8501
# - API Docs: http://localhost:8000/api/docs
```

### 2. Production Deployment (Budget Option)

#### Option A: DigitalOcean App Platform (~$30/month)
```bash
# Install doctl CLI
# Create app.yaml based on docker-compose.yml
doctl apps create --spec app.yaml
```

#### Option B: Railway.app (~$20/month)
```bash
# Install Railway CLI
railway login
railway up
```

#### Option C: Fly.io (~$25/month)
```bash
# Install flyctl
flyctl launch
flyctl deploy
```

## Project Structure

```
bootstrap_platform/
├── api/                    # FastAPI backend
│   ├── main.py           # Main API application
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Container config
├── admin/                  # Streamlit admin panel
│   ├── admin.py          # Admin interface
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile        # Container config
├── landing_page/          # Marketing website
│   └── index.html        # Single-page site
├── dashboard/             # Demo dashboard
│   └── dashboard.html    # Interactive demo
├── api_docs/              # API documentation
│   └── index.html        # Beautiful docs
├── webhook_tester/        # Webhook testing tool
│   └── index.html        # Testing interface
├── sdk_examples/          # Code examples
│   ├── python_quickstart.py
│   └── javascript_quickstart.js
├── nginx/                 # Web server config
│   └── nginx.conf        # Routing rules
├── docker-compose.yml     # Local development
└── README.md             # This file
```

## Key Features for Demos

### 1. Impressive Landing Page
- Professional design with animations
- ROI calculator
- Testimonials
- Integration showcase

### 2. Powerful API
- RESTful design
- OpenAPI documentation
- Fake data generation
- Working calculations

### 3. Beautiful Dashboard
- Real-time metrics
- Interactive charts
- Professional UI
- Mobile responsive

### 4. Admin Panel
- Lead management
- Demo environment builder
- Sales tools
- ROI calculator

## Demo Script

### For Sales Calls

1. **Start with the landing page**
   - Show ROI calculator
   - Highlight integrations
   - Point out testimonials

2. **Show the dashboard**
   - "This is what your team would see"
   - Click through metrics
   - Show real-time updates

3. **Demonstrate API**
   - Open API docs
   - Show code examples
   - "Your developers will love this"

4. **Close with pricing**
   - Emphasize setup fee
   - Monthly is "just maintenance"
   - "We customize everything for you"

## Configuration

### Environment Variables

```env
# API Configuration
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@db:5432/commission_iq
REDIS_URL=redis://redis:6379

# Admin Configuration
ADMIN_PASSWORD=your-admin-password

# Demo Mode
DEMO_MODE=true
FAKE_DATA=true
```

### SSL Certificates

For production:
```bash
# Using Let's Encrypt
certbot certonly --webroot -w /usr/share/nginx/html -d commission-intelligence.io
```

## Monitoring

### Basic Monitoring (Free)

1. **UptimeRobot** - Free uptime monitoring
2. **Sentry** - Free error tracking (up to 5k events)
3. **LogDNA** - Free log management (up to 1GB)

### Metrics Endpoint

```bash
curl http://localhost/api/health
```

## Scaling Strategy

When a customer pays:

1. **$2,500 Setup Fee**
   - Covers 1 integration build
   - 1 week development time

2. **$5,000 Setup Fee**
   - Covers 2 integrations
   - Custom features
   - 2-3 weeks development

3. **$10,000 Setup Fee**
   - Full platform customization
   - Multiple integrations
   - White label option
   - 4-6 weeks development

## Support

### For Demo Issues
- Check Docker logs: `docker-compose logs`
- Restart services: `docker-compose restart`
- Reset database: `docker-compose down -v && docker-compose up`

### For Customer Demos
- Use admin panel to create custom demos
- Modify fake data in `FakeDataGenerator`
- Customize colors in landing page

## Security Notes

⚠️ **For Production:**
- Change all default passwords
- Enable HTTPS only
- Set proper CORS origins
- Use real authentication
- Enable rate limiting
- Set up backups

## License

Proprietary - Commission Intelligence Platform 2024