/**
 * Shared Type Definitions for Multi-Tenant Education CRM SaaS.
 */

export interface TenantInfo {
  id: string;
  name: string;
  slug: string;
  customDomain?: string;
  tier: "standard" | "professional" | "enterprise";
  isActive: boolean;
}

export interface StudentProfile {
  id: string;
  tenantId: string;
  studentNumber: string;
  firstName: string;
  lastName: string;
  email: string;
  cgpa: number;
  creditsEarned: number;
  academicStanding: string;
  retentionRiskLevel: "low" | "moderate" | "high" | "critical";
}

export interface CourseCatalogItem {
  id: string;
  code: string;
  title: string;
  credits: number;
  departmentCode: string;
  level: number;
}

export interface InvoiceRecord {
  id: string;
  invoiceNumber: string;
  studentId: string;
  issueDate: string;
  dueDate: string;
  totalAmount: number;
  paidAmount: number;
  balanceAmount: number;
  status: "draft" | "issued" | "partially_paid" | "paid" | "overdue" | "cancelled";
}
