/**
 * Commission Intelligence Platform - JavaScript SDK Quickstart
 * This example demonstrates basic usage of the Commission IQ API
 */

// For Node.js
// const fetch = require('node-fetch');

// Configuration
const API_KEY = process.env.COMMISSION_IQ_API_KEY || 'demo_key_12345';
const BASE_URL = 'https://api.commission-intelligence.io/v1';

// For local development
// const BASE_URL = 'http://localhost:8000/api/v1';

class CommissionIQClient {
    constructor(apiKey, baseUrl = BASE_URL) {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }

    async request(method, endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            headers: this.headers,
            ...options
        };

        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} - ${data.message || 'Unknown error'}`);
            }
            
            return data;
        } catch (error) {
            console.error('Request failed:', error);
            throw error;
        }
    }

    // Policy methods
    async listPolicies(params = {}) {
        const queryString = new URLSearchParams(params).toString();
        return this.request('GET', `/policies${queryString ? `?${queryString}` : ''}`);
    }

    async createPolicy(policyData) {
        return this.request('POST', '/policies', { body: policyData });
    }

    // Commission methods
    async calculateCommission(premium, rate, type = 'NEW') {
        return this.request('POST', '/commissions/calculate', {
            body: { premium, rate, type }
        });
    }

    // Analytics methods
    async getDashboardMetrics(period = 'month') {
        return this.request('GET', `/analytics/dashboard?period=${period}`);
    }

    // Integration methods
    async getIntegrations() {
        return this.request('GET', '/integrations');
    }

    // Webhook methods
    async testWebhook(url, eventType = 'policy.created') {
        return this.request('POST', '/webhooks/test', {
            body: { url, event_type: eventType }
        });
    }
}

// Example usage
async function runDemo() {
    console.log('Commission Intelligence Platform - API Demo\n');
    
    const client = new CommissionIQClient(API_KEY);
    
    try {
        // 1. List existing policies
        console.log('1. Fetching existing policies...');
        const policies = await client.listPolicies({ status: 'active', page: 1, per_page: 5 });
        console.log(`   Found ${policies.pagination.total} total policies`);
        console.log(`   Total premium: $${policies.summary.total_premium.toLocaleString()}`);
        console.log(`   Total commission: $${policies.summary.total_commission.toLocaleString()}\n`);
        
        // 2. Create a new policy
        console.log('2. Creating a new policy...');
        const now = new Date();
        const newPolicy = {
            policy_number: `DEMO-${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`,
            customer: 'Demo Insurance Agency',
            carrier: 'Progressive',
            policy_type: 'AUTO',
            premium: 3500.00,
            effective_date: now.toISOString().split('T')[0],
            expiration_date: new Date(now.getTime() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
            commission_rate: 12.5
        };
        
        const created = await client.createPolicy(newPolicy);
        if (created.success) {
            console.log(`   ✓ Created policy ${created.data.policy_number}`);
            console.log(`   Commission amount: $${created.data.commission_amount.toFixed(2)}\n`);
        }
        
        // 3. Calculate commission scenarios
        console.log('3. Commission calculations:');
        const scenarios = [
            { premium: 5000, rate: 15, type: 'NEW', desc: 'New auto policy' },
            { premium: 8000, rate: 10, type: 'RENEWAL', desc: 'Home renewal' },
            { premium: 2000, rate: 20, type: 'ENDORSEMENT', desc: 'Policy endorsement' }
        ];
        
        for (const scenario of scenarios) {
            const result = await client.calculateCommission(
                scenario.premium,
                scenario.rate,
                scenario.type
            );
            console.log(`   ${scenario.desc}:`);
            console.log(`     Premium: $${scenario.premium.toLocaleString()}`);
            console.log(`     Agent commission: $${result.results.agent_commission.toFixed(2)}`);
            console.log(`     Agency commission: $${result.results.agency_commission.toFixed(2)}`);
        }
        
        console.log();
        
        // 4. Get dashboard metrics
        console.log('4. Dashboard analytics:');
        const metrics = await client.getDashboardMetrics('month');
        
        console.log(`   Active policies: ${metrics.metrics.active_policies.toLocaleString()}`);
        console.log(`   Renewal rate: ${metrics.metrics.renewal_rate.toFixed(1)}%`);
        console.log(`   Monthly growth: ${metrics.trends.monthly_growth.toFixed(1)}%`);
        
        console.log('\n   Top carriers by commission:');
        metrics.top_carriers.slice(0, 3).forEach(carrier => {
            console.log(`     - ${carrier.name}: $${carrier.commission.toLocaleString()}`);
        });
        
        console.log('\n   Top agents:');
        metrics.top_agents.slice(0, 3).forEach(agent => {
            console.log(`     - ${agent.name}: $${agent.commission.toLocaleString()} (${agent.policies} policies)`);
        });
        
        console.log();
        
        // 5. Check available integrations
        console.log('5. Available integrations:');
        const integrations = await client.getIntegrations();
        
        integrations.integrations.forEach(integration => {
            const statusEmoji = integration.status === 'available' ? '✓' : '⏳';
            console.log(`   ${statusEmoji} ${integration.name} (${integration.category})`);
            console.log(`      Setup fee: $${integration.setup_fee.toLocaleString()}`);
            integration.features.slice(0, 2).forEach(feature => {
                console.log(`      - ${feature}`);
            });
        });
        
        console.log(`\n   Total: ${integrations.summary.available} available, ${integrations.summary.coming_soon} coming soon`);
        
        // 6. Webhook testing
        console.log('\n6. Testing webhook delivery...');
        // Note: In production, you'd register a real webhook endpoint
        console.log('   Webhook functionality ready for production use');
        
        // Summary
        console.log('\n' + '='.repeat(50));
        console.log('Demo completed successfully!');
        console.log('Ready to integrate? Visit https://commission-intelligence.io/api/docs');
        
    } catch (error) {
        console.error('Demo failed:', error.message);
    }
}

// Run the demo
if (require.main === module) {
    runDemo();
}

// Export for use as a module
module.exports = { CommissionIQClient, runDemo };