import React, { useEffect, useRef } from 'react'
import useResizeAware from 'react-resize-aware'
import PropTypes from 'prop-types'
import Neovis from 'neovis.js/dist/neovis.js'
import './NeoGraph.css'

let vis
let onSubmit

const NeoGraph = props => {
  const {
    width,
    height,
    containerId,
    neo4jUri,
    neo4jUser,
    neo4jPassword,
    infoPreId,
    onSubmitFunction
  } = props

  const visRef = useRef()
  onSubmit = onSubmitFunction

  useEffect(() => {
    const config = {
      container_id: visRef.current.id,
      server_url: neo4jUri,
      server_user: neo4jUser,
      server_password: neo4jPassword,
      arrows: true,
      labels: {
        Node: {
          caption: 'name',
          thickness: 'pagerank',
          font: {
            size: 20,
            color: '#421b75',
            strokeWidth: 0
          }
        }
      },
      relationships: {
        RELATIONS: {
          thickness: 'pagerank',
          sentence: 'sentence',
          caption: 'relation'
        }
      }
    }
    vis = new Neovis(config)
    vis.registerOnEvent('completed', () => {
      vis._network.on('click', (event) => {
        clickHandler(event, infoPreId)
      })
      vis._network.on('doubleClick', (event) => {
        doubleClickHandler(event)
      })
    })
    vis.render()
  }, [neo4jUri, neo4jUser, neo4jPassword, infoPreId])

  return (
    <div
      id={containerId}
      ref={visRef}
      className='Neovis'
      style={{
        width: `${width}px`,
        height: `${height}px`
      }}
    />
  )
}

NeoGraph.propTypes = {
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  containerId: PropTypes.string.isRequired,
  neo4jUri: PropTypes.string.isRequired,
  neo4jUser: PropTypes.string.isRequired,
  neo4jPassword: PropTypes.string.isRequired,
  infoPreId: PropTypes.string
}

const ResponsiveNeoGraph = props => {
  const [resizeListener, sizes] = useResizeAware()

  const side = Math.max(sizes.width, sizes.height) / 2
  const neoGraphProps = { ...props, width: side * 1.99, height: side * 0.6 }
  return (
    <div style={{ position: 'relative' }}>
      {resizeListener}
      <NeoGraph {...neoGraphProps} />
    </div>
  )
}

ResponsiveNeoGraph.propTypes = {
  containerId: PropTypes.string.isRequired,
  neo4jUri: PropTypes.string.isRequired,
  neo4jUser: PropTypes.string.isRequired,
  neo4jPassword: PropTypes.string.isRequired,
  infoPreId: PropTypes.string
}

function parseEdgeTitle (title) {
  const result = { sentence: '', url: '', relation: '' }
  const data = title.match('^<strong>sentence:</strong> (.*)<br><strong>relation_url:</strong> (.*)<br><strong>relation:</strong> (.*)<br>$')
  if (data.length === 4) {
    result.sentence = data[1]
    result.url = data[2]
    result.relation = data[3]
  }
  return result
}

function clickHandler (event, infoPreId) {
  if (event.nodes[0] !== undefined) {
    const properties = vis._network.body.nodes[event.nodes[0]].options.raw.properties
    let text = properties.name
    if (properties.url !== '') {
      text = `<a href=${properties.url}>${text}</a>`
    }
    document.getElementById(infoPreId).innerHTML = text
  } else if (event.edges[0] !== undefined) {
    const edge = vis._network.body.edges[event.edges[0]]
    const properties = parseEdgeTitle(edge.title)
    let relation = `${edge.from.options.raw.properties.name} ——${properties.relation}—→ ${edge.to.options.raw.properties.name}`
    if (properties.url !== '') {
      relation = `<a href=${properties.url}>${relation}</a>`
    }
    document.getElementById(infoPreId).innerHTML = `${relation}<br>${properties.sentence}`
  }
}

function doubleClickHandler (event) {
  if (event.nodes[0] !== undefined) {
    onSubmit(vis._network.body.nodes[event.nodes[0]].options.raw.properties.name)
  }
}

function showAll () {
  vis.renderWithCypher('Match (n)-[r]->(m) Return *')
}

function stabilize () {
  vis.stabilize()
}

function clearAll () {
  vis.renderWithCypher('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r')
}

function hideAll (name) {
  vis.clearNetwork()
}

function updateGraph (name) {
  vis.updateWithCypher(`MATCH (n {name:"${name}"})-[*]-(connected) Match ()-[r:RELATIONS]->() Return *`)
}

export { ResponsiveNeoGraph, showAll, stabilize, clearAll, hideAll, updateGraph }
