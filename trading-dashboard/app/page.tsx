export default function Home() {
  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white mb-4">₿ Trading Dashboard</h1>
        <p className="text-xl text-slate-400 mb-8">Real-Time Bitcoin Analytics</p>
        <div className="bg-slate-800 p-8 rounded-lg max-w-md">
          <p className="text-slate-300 mb-4">Current BTC Price: <span className="text-green-400 font-bold">Loading...</span></p>
          <p className="text-slate-300 mb-4">Portfolio Balance: <span className="text-blue-400 font-bold">$93.75</span></p>
          <p className="text-slate-300">Status: <span className="text-yellow-400 font-bold">Ready to Trade</span></p>
        </div>
      </div>
    </div>
  )
}
