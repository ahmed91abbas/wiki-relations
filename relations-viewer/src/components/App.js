import React, { useState } from 'react'

import getRelations from '../api/relationsFinderApi'
import { ResponsiveNeoGraph, reload, stabilize, clearAll } from './NeoGraph'

const NEO4J_URI = process.env.REACT_APP_NEO4J_URI
const NEO4J_USER = process.env.REACT_APP_NEO4J_USER
const NEO4J_PASSWORD = process.env.REACT_APP_NEO4J_PASSWORD

async function onSubmit (title) {
  clearAll()
  await getRelations(title)
  reload()
}

const App = () => {
  const [input, setInput] = useState('')
  return (
    <div className='App' style={{ fontFamily: 'Quicksand' }}>
      <button onClick={stabilize}>Stabilize</button>
      <button onClick={clearAll}>Clear all</button>
      <h2>Person name:</h2>
      <input type='text' onInput={e => setInput(e.target.value)} style={{ width: '40%' }} />
      <button onClick={() => onSubmit(input)} style={{ width: '10%' }}>
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
