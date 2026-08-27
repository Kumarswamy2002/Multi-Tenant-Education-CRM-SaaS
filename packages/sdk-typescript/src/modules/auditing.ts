/**
 * CampusSphere TypeScript SDK Module: Auditing
 */

export interface AuditingRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class AuditingApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/auditing/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/auditing/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<AuditingRecord>) {
    return this.client.request(`/api/v1/auditing/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<AuditingRecord>) {
    return this.client.request(`/api/v1/auditing/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/auditing/${id}`, {
      method: "DELETE"
    });
  }
}
