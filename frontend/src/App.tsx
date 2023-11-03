

import leaderboard from './assets/leaderboard.svg'
import graph from './assets/graph.svg'
import cog from './assets/cog.svg'

function App() {

  return (
    <>
      <div className="flex flex-row justify-center h-20 w-auto">
        <button className="bg-navbut w-60 mr-5 sm:mr-10 rounded-b border-l border-r border-b-4 border-black" onClick={() => {}}>
          <img src={leaderboard} className="m-auto h-12 w-12" alt="Leaderboard icon" />
        </button>
        <button className="bg-navbut w-60 mr-5 sm:mr-10 rounded-b border-l border-r border-b-4 border-black" onClick={() => {}}>
          <img src={graph} className="m-auto h-12 w-12" alt="Graph icon" />
        </button>
        <button className="bg-navbut w-60 rounded-b border-l border-r border-b-4 border-black" onClick={() => {}}>
          <img src={cog} className="m-auto h-12 w-12" alt="Settings icon" />
        </button>
      </div>
    </>
  )
}

export default App
