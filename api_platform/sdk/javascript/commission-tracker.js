/**
 * Commission Intelligence Platform JavaScript SDK
 * Easy-to-use client for integrating with the Commission Tracker API
 */

class CommissionTracker {
    /**
     * Initialize the Commission Tracker client
     * @param {string} apiKey - Your API key from the Commission Tracker dashboard
     * @param {string} baseUrl - API base URL (defaults to production)
     */
    constructor(apiKey, baseUrl = 'https://api.commissiontracker.io') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'CommissionTrackerSDK/JS/1.0'
        };
    }

    /**
     * Make HTTP request to API
     * @private
     */
    async _request(method, endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        const fetchOptions = {
            method,
            headers: this.headers,
            ...options
        };

        if (options.body) {
            fetchOptions.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, fetchOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new CommissionTrackerError(
                    `API Error ${response.status}: ${data.error?.message || response.statusText}`,
                    response.status
                );
            }

            return data;
        } catch (error) {
            if (error instanceof CommissionTrackerError) {
                throw error;
            }
            throw new CommissionTrackerError(`Request failed: ${error.message}`);
        }
    }

    /**
     * Build query string from params object
     * @private
     */
    _buildQueryString(params) {
        if (!params || Object.keys(params).length === 0) return '';
        return '?' + new URLSearchParams(params).toString();
    }

    // Policy Management

    /**
     * List all policies
     * @param {Object} options - Query options
     * @param {number} options.page - Page number (default: 1)
     * @param {number} options.perPage - Items per page (default: 20)
     * @param {string} options.status - Filter by status
     */
    async listPolicies({ page = 1, perPage = 20, status } = {}) {
        const params = { page, per_page: perPage };
        if (status) params.status = status;
        
        const query = this._buildQueryString(params);
        return this._request('GET', `/v1/policies${query}`);
    }

    /**
     * Get a specific policy
     * @param {string} policyId - Policy ID
     */
    async getPolicy(policyId) {
        return this._request('GET', `/v1/policies/${policyId}`);
    }

    /**
     * Create a new policy
     * @param {Object} policyData - Policy data
     */
    async createPolicy(policyData) {
        return this._request('POST', '/v1/policies', { body: policyData });
    }

    /**
     * Update an existing policy
     * @param {string} policyId - Policy ID
     * @param {Object} policyData - Updated policy data
     */
    async updatePolicy(policyId, policyData) {
        return this._request('PUT', `/v1/policies/${policyId}`, { body: policyData });
    }

    /**
     * Delete a policy
     * @param {string} policyId - Policy ID
     */
    async deletePolicy(policyId) {
        return this._request('DELETE', `/v1/policies/${policyId}`);
    }

    // Commission Calculations

    /**
     * Calculate commission for given parameters
     * @param {Object} params - Calculation parameters
     * @param {number} params.premium - Premium amount
     * @param {number} params.rate - Commission rate percentage
     * @param {string} params.policyType - Type of policy (default: 'AUTO')
     * @param {string} params.transactionType - Transaction type (default: 'NEW')
     */
    async calculateCommission({ premium, rate, policyType = 'AUTO', transactionType = 'NEW' }) {
        return this._request('POST', '/v1/commissions/calculate', {
            body: {
                premium,
                commission_rate: rate,
                policy_type: policyType,
                transaction_type: transactionType
            }
        });
    }

    /**
     * Get pending commissions
     */
    async getPendingCommissions() {
        return this._request('GET', '/v1/commissions/pending');
    }

    // Analytics

    /**
     * Get analytics summary
     * @param {Object} options - Query options
     * @param {string} options.startDate - Start date (ISO format)
     * @param {string} options.endDate - End date (ISO format)
     */
    async getAnalyticsSummary({ startDate, endDate } = {}) {
        const params = {};
        if (startDate) params.start_date = startDate;
        if (endDate) params.end_date = endDate;
        
        const query = this._buildQueryString(params);
        return this._request('GET', `/v1/analytics/summary${query}`);
    }

    /**
     * Get agent performance metrics
     * @param {string} agentId - Agent ID
     * @param {string} period - Time period (default: 'month')
     */
    async getAgentPerformance(agentId, period = 'month') {
        const query = this._buildQueryString({ period });
        return this._request('GET', `/v1/analytics/agent/${agentId}${query}`);
    }

    // Webhooks

    /**
     * Create a new webhook
     * @param {Object} params - Webhook parameters
     * @param {string} params.url - Webhook endpoint URL
     * @param {string[]} params.events - Events to subscribe to
     * @param {string} params.secret - Optional webhook secret
     */
    async createWebhook({ url, events, secret }) {
        const body = { url, events };
        if (secret) body.secret = secret;
        
        return this._request('POST', '/v1/webhooks', { body });
    }

    /**
     * List all webhooks
     */
    async listWebhooks() {
        return this._request('GET', '/v1/webhooks');
    }

    /**
     * Delete a webhook
     * @param {string} webhookId - Webhook ID
     */
    async deleteWebhook(webhookId) {
        return this._request('DELETE', `/v1/webhooks/${webhookId}`);
    }
}

class CommissionTrackerError extends Error {
    constructor(message, statusCode = null) {
        super(message);
        this.name = 'CommissionTrackerError';
        this.statusCode = statusCode;
    }
}

// Export for different environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommissionTracker;
} else if (typeof window !== 'undefined') {
    window.CommissionTracker = CommissionTracker;
}

// Example usage
/*
const client = new CommissionTracker('your_api_key_here');

// List policies
const policies = await client.listPolicies({ page: 1, perPage: 20 });
console.log(`Found ${policies.length} policies`);

// Create a policy
const newPolicy = await client.createPolicy({
    policy_number: 'AUTO-123456',
    customer: 'John Doe',
    effective_date: '2025-09-01',
    premium: 1200.00,
    commission_rate: 12.0
});
console.log(`Created policy: ${newPolicy.id}`);

// Calculate commission
const commission = await client.calculateCommission({
    premium: 1200.00,
    rate: 12.0,
    policyType: 'AUTO',
    transactionType: 'NEW'
});
console.log(`Commission: $${commission.agent_commission}`);
*/