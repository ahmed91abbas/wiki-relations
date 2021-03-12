import React, { useState } from 'react'
import './App.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrash, faEye, faEyeSlash, faEquals } from '@fortawesome/free-solid-svg-icons'

import getRelations from '../api/relationsFinderApi'
import { ResponsiveNeoGraph, showAll, stabilize, clearAll, hideAll, updateGraph } from './NeoGraph'

const NEO4J_URI = process.env.REACT_APP_NEO4J_URI
const NEO4J_USER = process.env.REACT_APP_NEO4J_USER
const NEO4J_PASSWORD = process.env.REACT_APP_NEO4J_PASSWORD

const INFO_PRE_ID = 'infoPreId'
const INFO_ID = 'infoId'

async function onSubmit (title) {
  const element = document.getElementById('submitBtn')
  element.classList.add('is-loading')
  const response = await getRelations(title)
  element.classList.remove('is-loading')
  if (response) {
    updateGraph(response.subject)
  }
}

function handleKeyPress (event) {
  if (event.key === 'Enter') {
    document.getElementById('submitBtn').click()
  }
}

function resetValues () {
  document.getElementById(INFO_ID).value = ''
  document.getElementById(INFO_PRE_ID).innerHTML = ''
}

function onHideAll () {
  resetValues()
  hideAll()
}

function onClearAll () {
  resetValues()
  clearAll()
}

const App = () => {
  const [input, setInput] = useState('')
  return (
    <div>
      <pre className='bg' />
      <div className='padding'>
        <input className='input is-link is-medium input-custom' id={INFO_ID} type='text' placeholder='Enter name' onKeyPress={handleKeyPress} onInput={e => setInput(e.target.value)} />
        <button className='button is-medium is-link submit-button' id='submitBtn' onClick={() => onSubmit(input)}>Submit</button>
        <div className='buttons are-medium align-right'>
          <button className='button is-rounded is-dark' onClick={stabilize}>
            <span className='icon'><i><FontAwesomeIcon icon={faEquals} /></i></span>
          </button>
          <button className='button is-rounded is-dark' onClick={showAll}>
            <span className='icon'><i><FontAwesomeIcon icon={faEye} /></i></span>
          </button>
          <button className='button is-rounded is-dark' onClick={onHideAll}>
            <span className='icon'><i><FontAwesomeIcon icon={faEyeSlash} /></i></span>
          </button>
          <button className='button is-rounded is-dark' onClick={onClearAll}>
            <span className='icon'><i><FontAwesomeIcon icon={faTrash} /></i></span>
          </button>
        </div>
        <pre className='bg' />
      </div>
      <ResponsiveNeoGraph
        containerId='neovis'
        neo4jUri={NEO4J_URI}
        neo4jUser={NEO4J_USER}
        neo4jPassword={NEO4J_PASSWORD}
        infoPreId={INFO_PRE_ID}
      />
      <pre className='padding info bg' id={INFO_PRE_ID} />
    </div>
  )
}

export default App
