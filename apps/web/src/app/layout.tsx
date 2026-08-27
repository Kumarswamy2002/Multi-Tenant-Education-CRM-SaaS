import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CampusSphere CRM | Multi-Tenant Education Relationship Platform',
  description: 'Enterprise Multi-Tenant Education CRM SaaS managing the complete learner lifecycle.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased text-slate-900 bg-slate-50">
        {children}
      </body>
    </html>
  );
}
