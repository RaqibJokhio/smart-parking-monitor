export default function LiveFeed({ videoPath = "data/sample.mp4" }) {
  const src = `/api/video/stream?video_path=${encodeURIComponent(videoPath)}`

  return (
    <div className="bg-gray-800 rounded-xl p-5 shadow">
      <p className="text-gray-400 text-sm mb-3">Live Feed</p>
      <img
        src={src}
        alt="Live parking feed"
        className="w-full rounded-lg border border-gray-700"
      />
    </div>
  )
}