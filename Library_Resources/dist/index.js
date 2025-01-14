addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  return new Response('iHelper: Biz-Builder Resource Library', {
    headers: { 'Content-Type': 'text/html' }
  })
}
