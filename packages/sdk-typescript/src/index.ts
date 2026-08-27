/**
 * CampusSphere Official TypeScript / JavaScript Client SDK.
 */
export interface CampusSphereConfig {
  apiKey: string;
  baseUrl?: string;
  tenantId?: string;
}

export class CampusSphereClient {
  private apiKey: string;
  private baseUrl: string;
  private tenantId: string;

  constructor(config: CampusSphereConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = (config.baseUrl || "http://localhost:8000/api/v1").replace(/\/$/, "");
    this.tenantId = config.tenantId || "default-tenant";
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      "Authorization": `Bearer ${this.apiKey}`,
      "X-Tenant-ID": this.tenantId,
      "Content-Type": "application/json",
      ...options.headers,
    };

    const res = await fetch(url, { ...options, headers });
    if (!res.ok) {
      throw new Error(`CampusSphere API Error [${res.status}]: ${await res.text()}`);
    }
    return res.json();
  }

  async getAcademicsList() {
    return this.request<{ success: boolean; data: any[] }>("/academics/list");
  }

  async getBillingInvoices() {
    return this.request<{ success: boolean; data: any[] }>("/billing-finance/list");
  }

  async predictRetentionRisk(studentId: string) {
    return this.request<{ success: boolean; data: any }>("/ai-insights/action/execute", {
      method: "POST",
      body: JSON.stringify({ action_type: "retention_predict", record_ids: [studentId] })
    });
  }
}
