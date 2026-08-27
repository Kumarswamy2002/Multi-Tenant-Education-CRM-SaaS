/**
 * CampusSphere TypeScript SDK Module: Academics
 */

export interface AcademicsRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class AcademicsApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/academics/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/academics/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<AcademicsRecord>) {
    return this.client.request(`/api/v1/academics/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<AcademicsRecord>) {
    return this.client.request(`/api/v1/academics/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/academics/${id}`, {
      method: "DELETE"
    });
  }
}
