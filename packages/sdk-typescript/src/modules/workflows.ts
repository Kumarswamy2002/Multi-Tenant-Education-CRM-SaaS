/**
 * CampusSphere TypeScript SDK Module: Workflows
 */

export interface WorkflowsRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class WorkflowsApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/workflows/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/workflows/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<WorkflowsRecord>) {
    return this.client.request(`/api/v1/workflows/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<WorkflowsRecord>) {
    return this.client.request(`/api/v1/workflows/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/workflows/${id}`, {
      method: "DELETE"
    });
  }
}
