/**
 * CampusSphere TypeScript SDK Module: Settings
 */

export interface SettingsRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class SettingsApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/settings/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/settings/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<SettingsRecord>) {
    return this.client.request(`/api/v1/settings/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<SettingsRecord>) {
    return this.client.request(`/api/v1/settings/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/settings/${id}`, {
      method: "DELETE"
    });
  }
}
