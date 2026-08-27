/**
 * CampusSphere TypeScript SDK Module: Employers
 */

export interface EmployersRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class EmployersApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/employers/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/employers/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<EmployersRecord>) {
    return this.client.request(`/api/v1/employers/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<EmployersRecord>) {
    return this.client.request(`/api/v1/employers/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/employers/${id}`, {
      method: "DELETE"
    });
  }
}
