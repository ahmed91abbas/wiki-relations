require('isomorphic-fetch')

export default async function submitRequest (title) {
  if (title === '') return
  const url = `${process.env.REACT_APP_RELATIONS_FINDER_URI}/relations-finder`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title: title })
  })
  console.log(response)
}
