/**
 * CampusSphere TypeScript SDK Module: Library
 */

export interface LibraryRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class LibraryApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/library/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/library/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<LibraryRecord>) {
    return this.client.request(`/api/v1/library/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<LibraryRecord>) {
    return this.client.request(`/api/v1/library/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/library/${id}`, {
      method: "DELETE"
    });
  }
}
