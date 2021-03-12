import React, { useState } from 'react'
import './App.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrash, faEye, faEyeSlash, faEquals } from '@fortawesome/free-solid-svg-icons'

import getRelations from '../api/relationsFinderApi'
import { ResponsiveNeoGraph, showAll, stabilize, clearAll, hideAll, updateGraph } from './NeoGraph'

const NEO4J_URI = process.env.REACT_APP_NEO4J_URI
const NEO4J_USER = process.env.REACT_APP_NEO4J_USER
const NEO4J_PASSWORD = process.env.REACT_APP_NEO4J_PASSWORD

async function onSubmit (title) {
  const element = document.getElementById('submitBtn')
  element.classList.add('is-loading')
  const response = await getRelations(title)
  element.classList.remove('is-loading')
  updateGraph(response.subject)
}

function handleKeyPress (event) {
  if (event.key === 'Enter') {
    document.getElementById('submitBtn').click()
  }
}

const App = () => {
  const [input, setInput] = useState('')
  const infoPreId = 'infoPreId'
  return (
    <div>
      <pre className='bg' />
      <div className='padding'>
        <input className='input is-link is-medium input-custom' type='text' placeholder='Enter name' onKeyPress={handleKeyPress} onInput={e => setInput(e.target.value)} />
        <button className='button is-medium is-link submit-button' id='submitBtn' onClick={() => onSubmit(input)}>Submit</button>
        <div class='buttons are-medium align-right'>
          <button class='button is-rounded is-dark' onClick={stabilize}>
            <span class='icon'><i><FontAwesomeIcon icon={faEquals} /></i></span>
          </button>
          <button class='button is-rounded is-dark' onClick={showAll}>
            <span class='icon'><i><FontAwesomeIcon icon={faEye} /></i></span>
          </button>
          <button class='button is-rounded is-dark' onClick={hideAll}>
            <span class='icon'><i><FontAwesomeIcon icon={faEyeSlash} /></i></span>
          </button>
          <button class='button is-rounded is-dark' onClick={clearAll}>
            <span class='icon'><i><FontAwesomeIcon icon={faTrash} /></i></span>
          </button>
        </div>
        <pre className='bg' />
      </div>
      <ResponsiveNeoGraph
        containerId='neovis'
        neo4jUri={NEO4J_URI}
        neo4jUser={NEO4J_USER}
        neo4jPassword={NEO4J_PASSWORD}
        infoPreId={infoPreId}
      />
      <pre className='padding info bg' id={infoPreId} />
    </div>
  )
}

export default App
