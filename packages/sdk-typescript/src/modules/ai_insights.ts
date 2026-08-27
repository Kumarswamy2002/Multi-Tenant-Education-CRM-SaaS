/**
 * CampusSphere TypeScript SDK Module: Ai Insights
 */

export interface AiInsightsRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class AiInsightsApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/ai-insights/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/ai-insights/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<AiInsightsRecord>) {
    return this.client.request(`/api/v1/ai-insights/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<AiInsightsRecord>) {
    return this.client.request(`/api/v1/ai-insights/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/ai-insights/${id}`, {
      method: "DELETE"
    });
  }
}
