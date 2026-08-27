/**
 * CampusSphere TypeScript SDK Module: Grading
 */

export interface GradingRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class GradingApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/grading/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/grading/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<GradingRecord>) {
    return this.client.request(`/api/v1/grading/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<GradingRecord>) {
    return this.client.request(`/api/v1/grading/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/grading/${id}`, {
      method: "DELETE"
    });
  }
}
