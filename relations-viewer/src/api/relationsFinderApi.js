require('isomorphic-fetch')

export default async function submitRequest (title) {
  if (title === '') return false
  const url = `${process.env.REACT_APP_RELATIONS_FINDER_URI}/relations-finder`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title: title })
  })

  if (response.status === 200) {
    return response.json()
  }
  return false
}
