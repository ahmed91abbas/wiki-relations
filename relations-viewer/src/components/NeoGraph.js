import React, { useEffect, useRef } from 'react'
import useResizeAware from 'react-resize-aware'
import PropTypes from 'prop-types'
import Neovis from 'neovis.js/dist/neovis.js'

let vis

const NeoGraph = props => {
  const {
    width,
    height,
    containerId,
    backgroundColor,
    neo4jUri,
    neo4jUser,
    neo4jPassword,
    infoPreId
  } = props

  const visRef = useRef()

  useEffect(() => {
    const config = {
      container_id: visRef.current.id,
      server_url: neo4jUri,
      server_user: neo4jUser,
      server_password: neo4jPassword,
      arrows: true,
      initial_cypher: 'Match (n)-[r]->(m) Return n,r,m'
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
      style={{
        width: `${width}px`,
        height: `${height}px`,
        backgroundColor: `${backgroundColor}`,
        border: '5px solid black'
      }}
    />
  )
}

NeoGraph.defaultProps = {
  width: 600,
  height: 600,
  backgroundColor: '#d3d3d3'
}

NeoGraph.propTypes = {
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  containerId: PropTypes.string.isRequired,
  neo4jUri: PropTypes.string.isRequired,
  neo4jUser: PropTypes.string.isRequired,
  neo4jPassword: PropTypes.string.isRequired,
  backgroundColor: PropTypes.string,
  infoPreId: PropTypes.string
}

const ResponsiveNeoGraph = props => {
  const [resizeListener, sizes] = useResizeAware()

  const side = Math.max(sizes.width, sizes.height) / 2
  const neoGraphProps = { ...props, width: side * 1.2, height: side / 1.2 }
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
  backgroundColor: PropTypes.string,
  infoPreId: PropTypes.string
}

function clickHandler (event, infoPreId) {
  if (event.nodes[0]) {
    document.getElementById(infoPreId).innerHTML = vis._network.body.nodes[event.nodes[0]].options.title
  } else if (event.edges[0]) {
    document.getElementById(infoPreId).innerHTML = vis._network.body.edges[event.edges[0]].options.title
  }
}

function doubleClickHandler (event) {
  if (event.nodes[0]) {
    const name = vis._network.body.nodes[event.nodes[0]].options.raw.properties.name
    console.log(name)
  }
}

function reload () {
  vis.renderWithCypher('Match (n)-[r]->(m) Return n,r,m')
}

function stabilize () {
  vis.stabilize()
}

function clearAll () {
  vis.renderWithCypher('MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n, r')
}

export { ResponsiveNeoGraph, reload, stabilize, clearAll }
