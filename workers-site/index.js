addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  // Basic routing for templates
  if (request.url.includes('/templates')) {
    const templateData = await fetchTemplateData()
    return new Response(JSON.stringify(templateData), {
      headers: { 'Content-Type': 'application/json' }
    })
  }
  
  // Default response
  return new Response('Templates Service', { status: 200 })
}

async function fetchTemplateData() {
  // In a real-world scenario, this would fetch from your metadata JSON
  return {
    templates: [
      { id: 1, name: 'Introduction Template', category: 'Fundamentals' }
    ]
  }
}
