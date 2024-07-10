let ledStatus = false

const ledToggleButton = document.getElementById('led-toggle-button')
ledToggleButton.disabled = true

function fetchAndUpdateLEDStatus() {
    const evtSource = new EventSource('/events')

    evtSource.onmessage = function(event) {
        ledStatus = event.data === 'ON'
        updateLEDUI()
    }

    evtSource.onerror = function() {
        console.error('EventSource failed.')
        evtSource.close()
    }
}

function updateLEDUI() {
    const ledOn = document.getElementById('led-on')
    const ledOff = document.getElementById('led-off')
    const ledToggleButton = document.getElementById('led-toggle-button')

    const oldLedOn = ledOn.cloneNode(true)
    const oldLedOff = ledOff.cloneNode(true)
    ledOn.parentNode.replaceChild(oldLedOn, ledOn)
    ledOff.parentNode.replaceChild(oldLedOff, ledOff)

    const applyHoverEffect = () => {
        ledToggleButton.classList.add('led')
    }
    const removeHoverEffect = () => {
        ledToggleButton.classList.remove('led')
    }

    if (ledStatus) {
        oldLedOff.style.borderRadius = '0 8px 8px 0'
        oldLedOff.style.backgroundColor = '#3f3f46'
        oldLedOff.style.color = '#a1a1aa'
        oldLedOff.classList.add('led')
        oldLedOn.style.borderRadius = '8px'
        oldLedOn.style.backgroundColor = '#15803d'
        oldLedOn.style.color = '#f8fafc'
        oldLedOn.classList.remove('led')

        oldLedOff.addEventListener('mouseover', applyHoverEffect)
        oldLedOff.addEventListener('mouseout', removeHoverEffect)

        oldLedOff.addEventListener('click', applyHoverEffect)
        oldLedOff.addEventListener('click', removeHoverEffect)
    } else {
        oldLedOff.style.borderRadius = '8px'
        oldLedOff.style.backgroundColor = '#dc2626'
        oldLedOff.style.color = '#f8fafc'
        oldLedOff.classList.remove('led')
        oldLedOn.style.borderRadius = '8px 0 0 8px'
        oldLedOn.style.backgroundColor = '#3f3f46'
        oldLedOn.style.color = '#a1a1aa'
        oldLedOn.classList.add('led')

        oldLedOn.addEventListener('mouseover', applyHoverEffect)
        oldLedOn.addEventListener('mouseout', removeHoverEffect)

        oldLedOn.addEventListener('click', applyHoverEffect)
        oldLedOn.addEventListener('click', removeHoverEffect)
    }
}

async function getInitialLEDStatus() {
    try {
        const response = await fetch('/get_status')
        const data = await response.json()
        ledStatus = data.status === 'ON'
        updateLEDUI()
    } catch (error) {
        console.error('Error fetching initial LED status:', error)
    }
}

async function toggleLED() {
    ledStatus = !ledStatus
    const action = ledStatus ? 'led=on' : 'led=off'
    try {
        await fetch(`/${action}`)
    } catch (error) {
        console.error('Error toggling LED:', error)
    }
}

document.addEventListener('DOMContentLoaded', () => {
    getInitialLEDStatus()
    fetchAndUpdateLEDStatus()
})

document.addEventListener('readystatechange', function () {
    const ledToggleButton = document.getElementById('led-toggle-button')

    if (document.readyState === 'complete') {
        ledToggleButton.disabled = false
        updateLEDUI()
        getInitialLEDStatus()
    }
})
