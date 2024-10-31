import React from 'react';
import { Server, Database, Shield, Clock, ArrowRight, File } from 'lucide-react';

export default function ArchitectureDiagram() {
  return (
    <div className="w-full h-96 bg-slate-50 p-4 rounded-lg shadow-sm">
      <div className="relative w-full h-full">
        {/* Client Layer */}
        <div className="absolute top-4 left-4 bg-white p-3 rounded-lg shadow-md w-48">
          <h3 className="text-sm font-semibold mb-2">Client Request</h3>
          <div className="flex items-center gap-2">
            <File size={20} className="text-blue-500" />
            <span className="text-sm">API Request</span>
          </div>
        </div>

        {/* FastAPI Layer */}
        <div className="absolute top-4 left-1/3 bg-white p-3 rounded-lg shadow-md w-48">
          <h3 className="text-sm font-semibold mb-2">Client Handler</h3>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <Server size={20} className="text-purple-500" />
              <span className="text-sm">FastAPI</span>
            </div>
          </div>
        </div>

        {/* Queue & Nginx Layer */}
        <div className="absolute top-32 left-1/3 bg-white p-3 rounded-lg shadow-md w-48">
          <h3 className="text-sm font-semibold mb-2">Middleware Layer</h3>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <Shield size={20} className="text-green-500" />
              <span className="text-sm">Nginx (Gateway)</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={20} className="text-orange-500" />
              <span className="text-sm">Main Queue</span>
            </div>
            <div className="flex items-center gap-2">
              <Clock size={20} className="text-yellow-500" />
              <span className="text-sm">Backup Queue</span>
            </div>
          </div>
        </div>

        {/* KIPRIS API Layer */}
        <div className="absolute right-4 top-4 bg-white p-3 rounded-lg shadow-md w-48">
          <h3 className="text-sm font-semibold mb-2">KIPRIS API</h3>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <Server size={20} className="text-indigo-500" />
              <span className="text-sm">External API</span>
            </div>
          </div>
        </div>

        {/* Database Layer */}
        <div className="absolute right-4 top-32 bg-white p-3 rounded-lg shadow-md w-48">
          <h3 className="text-sm font-semibold mb-2">Database</h3>
          <div className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <Database size={20} className="text-blue-500" />
              <span className="text-sm">SQLite</span>
            </div>
          </div>
        </div>

        {/* Flow Description */}
        <div className="absolute bottom-4 left-4 right-4 bg-white p-3 rounded-lg shadow-md">
          <h3 className="text-sm font-semibold mb-2">Data Flow</h3>
          <div className="text-xs text-gray-600 space-y-1">
            <p>1. Client 요청 → FastAPI (요청 처리)</p>
            <p>2. FastAPI → Nginx (KIPRIS API 통신 관리)</p>
            <p>3. Nginx ↔ KIPRIS API (실제 API 통신)</p>
            <p>4. FastAPI → Queue System (작업 관리)</p>
            <p>5. 결과 저장 → SQLite DB</p>
            <p>6. 응답 반환 → Client</p>
          </div>
        </div>
      </div>
    </div>
  );
}