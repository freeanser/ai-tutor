// src/app/page.tsx
'use client'; // 必須加上這一行，因為有使用 useState

import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

export default function Home() {
  const [essay, setEssay] = useState('');
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!essay) return alert("請輸入內容");
    setLoading(true);
    try {
      const res = await fetch('http://localhost:5001/api/grade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: essay }),
      });
      const data = await res.json();
      setFeedback(data.feedback);
    } catch (error) {
      console.error("連線失敗:", error);
      setFeedback("拍謝，後端還沒開或是連不上喔！");
    } finally {
      setLoading(false);
    }
  };
  return (
    <main className="min-h-screen bg-white p-8">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row gap-8"> {/* 改為 Flex 佈局 */}

        {/* 左側：輸入區 */}
        <div className="flex-1">
          <h1 className="text-3xl font-bold mb-6 text-slate-800">AI 英文作文批改</h1>
          <textarea
            className="w-full h-[500px] p-4 border-2 border-slate-200 rounded-lg focus:border-blue-500 outline-none text-black"
            value={essay}
            onChange={(e) => setEssay(e.target.value)}
            placeholder="請在此輸入英文作文..."
          />
          <button
            onClick={handleSubmit}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition-colors disabled:bg-slate-400"
            disabled={loading}
          >
            {loading ? 'AI 正在思考中...' : '提交批改'}
          </button>
        </div>

        {/* 右側：AI 建議區 */}
        <div className="flex-1">
          <div className="h-full p-6 bg-slate-50 border border-slate-200 rounded-lg overflow-y-auto">
            <h2 className="font-bold mb-4 text-slate-700 text-xl border-b pb-2">批改建議</h2>
            {feedback ? (
              <div className="prose prose-slate max-w-none text-slate-600 leading-relaxed">
                {/* 使用 ReactMarkdown 解析內容 */}
                <ReactMarkdown>{feedback}</ReactMarkdown>
              </div>
            ) : (
              <p className="text-slate-400 italic">等待提交後顯示建議...</p>
            )}
          </div>
        </div>

      </div>
    </main>
  );
}