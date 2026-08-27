/**
 * CampusSphere TypeScript SDK Module: Schedules
 */

export interface SchedulesRecord {
  id: string;
  tenantId: string;
  name?: string;
  title?: string;
  status: string;
  createdAt: string;
  updatedAt: string;
  metadata?: Record<string, any>;
}

export class SchedulesApi {
  private client: any;

  constructor(client: any) {
    this.client = client;
  }

  async list(page = 1, pageSize = 50, filters?: Record<string, any>) {
    return this.client.request(`/api/v1/schedules/list`, {
      method: "GET",
      params: { page, pageSize, ...filters }
    });
  }

  async getById(id: string) {
    return this.client.request(`/api/v1/schedules/${id}`, {
      method: "GET"
    });
  }

  async create(payload: Partial<SchedulesRecord>) {
    return this.client.request(`/api/v1/schedules/`, {
      method: "POST",
      body: JSON.stringify(payload)
    });
  }

  async update(id: string, payload: Partial<SchedulesRecord>) {
    return this.client.request(`/api/v1/schedules/${id}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    });
  }

  async remove(id: string) {
    return this.client.request(`/api/v1/schedules/${id}`, {
      method: "DELETE"
    });
  }
}
