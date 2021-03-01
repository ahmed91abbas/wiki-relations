import React from 'react'
import { ResponsiveNeoGraph, reload, stabilize } from './NeoGraph'

const NEO4J_URI = 'bolt://localhost:7687'
const NEO4J_USER = 'neo4j'
const NEO4J_PASSWORD = 'test'

const App = () => {
  return (
    <div className='App' style={{ fontFamily: 'Quicksand' }}>
      <button onClick={stabilize}>Stabilize</button>
      <h2>Person name:</h2>
      <input type='text' id='person' style={{ width: '40%' }} />
      <button onClick={reload} style={{ width: '10%' }}>
        Submit
      </button>
      <pre />
      <ResponsiveNeoGraph
        containerId='neovis'
        neo4jUri={NEO4J_URI}
        neo4jUser={NEO4J_USER}
        neo4jPassword={NEO4J_PASSWORD}
        backgroundColor='#d3d3d3'
      />
    </div>
  )
}

export default App
