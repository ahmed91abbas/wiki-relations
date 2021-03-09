import React, { useState } from 'react'
import './App.css'

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

function handleKeyPress (event) {
  if (event.key === 'Enter') {
    document.getElementById('submitBtn').click()
  }
}

const App = () => {
  const [input, setInput] = useState('')
  const infoPreId = 'infoPreId'
  document.body.className = 'app'
  return (
    <div className='app'>
      <br /><br />
      <div className='padding'>
        <input className='input' type='text' placeholder='Enter name' onKeyPress={handleKeyPress} onInput={e => setInput(e.target.value)} />
        <button className='button submit-button' id='submitBtn' onClick={() => onSubmit(input)}>Submit</button>
        <button className='button align-right' onClick={clearAll}>Clear all</button>
        <button className='button align-right' onClick={stabilize}>Stabilize</button>
        <pre />
      </div>
      <ResponsiveNeoGraph
        containerId='neovis'
        neo4jUri={NEO4J_URI}
        neo4jUser={NEO4J_USER}
        neo4jPassword={NEO4J_PASSWORD}
        infoPreId={infoPreId}
      />
      <pre className='padding info' id={infoPreId} />
    </div>
  )
}

export default App
