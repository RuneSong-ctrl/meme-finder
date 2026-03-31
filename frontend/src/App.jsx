import { useState } from "react";
import axios from "axios";
import { Search, Loader2 } from "lucide-react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const response = await axios.get(
        `http://localhost:8000/search?query=${query}`,
      );
      setResults(response.data.results);
    } catch (error) {
      console.error(error);
      alert("Gagal menghubungi server. Pastikan backend menyala!");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-blue-200">
      <div className="fixed top-0 left-0 w-full h-96 bg-linear-to-b from-blue-100/50 to-transparent -z-10 pointer-events-none" />

      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="flex flex-col items-center text-center mb-16 mt-8 space-y-4">
          <h1 className="text-5xl font-extrabold tracking-tight text-slate-900">
            Meme<span className="text-blue-600 bg-clip-text">Search</span>
          </h1>
          <p className="text-lg text-slate-500 max-w-xl font-medium">
            Temukan meme yang tepat hanya dengan mendeskripsikan momennya.
          </p>
        </div>

        <form
          onSubmit={handleSearch}
          className="mb-16 flex justify-center w-full"
        >
          <div className="relative w-full max-w-3xl group">
            <div className="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none text-slate-400 group-focus-within:text-blue-500 transition-colors">
              <Search className="w-6 h-6" />
            </div>
            <input
              type="text"
              className="w-full pl-16 pr-32 py-5 text-lg bg-white border border-slate-200 rounded-full shadow-sm hover:shadow-md focus:shadow-xl focus:outline-none focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 transition-all duration-300 placeholder:text-slate-400"
              placeholder="Contoh: kucing menangis lihat makanan..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <div className="absolute inset-y-0 right-2 flex items-center">
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="flex items-center gap-2 px-8 py-3 bg-slate-900 hover:bg-blue-600 text-white rounded-full font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-md"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Mencari</span>
                  </>
                ) : (
                  <span>Cari</span>
                )}
              </button>
            </div>
          </div>
        </form>

        {loading && (
          <div className="flex flex-col items-center justify-center py-20 text-slate-400 space-y-4">
            <Loader2 className="w-10 h-10 animate-spin text-blue-500" />
            <p className="font-medium animate-pulse">
              Menghitung jarak vektor semantik...
            </p>
          </div>
        )}

        {!loading && hasSearched && results.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20 text-slate-400">
            <Search className="w-12 h-12 mb-4 opacity-20" />
            <p className="text-lg font-medium text-slate-500">
              Meme tidak ditemukan di database.
            </p>
          </div>
        )}

        <div className="columns-1 sm:columns-2 lg:columns-3 gap-6 space-y-6">
          {results.map((meme, index) => (
            <div
              key={index}
              className="relative group bg-slate-200 rounded-3xl overflow-hidden border border-slate-100 shadow-sm hover:shadow-2xl hover:-translate-y-1 transition-all duration-500 break-inside-avoid"
            >
              <img
                src={meme.image_url}
                alt={meme.filename}
                className="w-full h-auto block"
              />

              <div className="absolute inset-0 bg-slate-900/80 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-6">
                <div className="mb-2">
                  <span className="inline-block px-3 py-1 bg-blue-600 text-white text-sm font-bold rounded-full mb-3">
                    {/* Mengonversi skor CLIP (0.15 - 0.35) menjadi persentase 0-100% */}
                    {Math.min(
                      100,
                      Math.max(0, ((meme.score - 0.15) / 0.15) * 100),
                    ).toFixed(1)}
                    % Cocok
                  </span>
                </div>

                {meme.meme_text && (
                  <div className="mb-4">
                    <p className="text-slate-300 text-xs font-semibold uppercase tracking-wider mb-1">
                      Teks OCR
                    </p>
                    <p className="text-white text-sm italic font-medium">
                      "{meme.meme_text}"
                    </p>
                  </div>
                )}

                <div className="pt-4 border-t border-slate-700/50 flex flex-col gap-1.5">
                  <div className="flex justify-between items-center text-xs text-slate-300">
                    <span>File</span>
                    <span className="font-medium truncate max-w-37.5">
                      {meme.filename}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-300">
                    <span>Skor Visual</span>
                    <span className="font-medium">
                      {meme.visual_score.toFixed(3)}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-xs text-slate-300">
                    <span>Bonus Teks</span>
                    <span className="font-medium text-blue-400">
                      +{meme.text_boost.toFixed(3)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
