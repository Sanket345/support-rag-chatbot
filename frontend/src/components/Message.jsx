export default function Message({ message }) {
  const isUser = message.role === "user";

  const bubble = isUser
    ? "bg-indigo-600 text-white"
    : message.error
    ? "bg-red-50 text-red-700 border border-red-200"
    : "bg-white text-slate-800 border";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm md:max-w-[70%] ${bubble}`}>
        <p className="whitespace-pre-wrap leading-relaxed">{message.content}</p>

        {message.sources?.length > 0 && (
          <div className="mt-3 border-t pt-2">
            <p className="mb-1 text-xs font-medium text-slate-500">Sources</p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((s) => (
                <span
                  key={`${s.source}-${s.page}`}
                  className="rounded-full bg-indigo-50 px-2 py-1 text-xs text-indigo-700"
                >
                  📄 {s.source} · p.{s.page}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
