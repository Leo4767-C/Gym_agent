import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Personal Trainer 🏋️',
  description: 'AI-powered workout planner using RAG, Ollama, and ChromaDB',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
