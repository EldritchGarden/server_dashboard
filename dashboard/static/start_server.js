// used by index.html to control rendering for certain elements
// and handle server starting

async function fetch_state(id) {
    let response = await fetch(`/state/${id}`);
    let state = await response.text();

    return state;
}

async function unhide_elements() {
    let entries = document.getElementsByClassName('main');

    for (let item of entries) {
        let state = await fetch_state(item.id);
        console.log(`State of ${item.id} is ${state}`);

        // default state shows offline icon and disabled button.
        // start button is only enabled if state is 'offline' to help
        //   prevent multiple signals.
        // if in an ephemeral state (starting, stopping) show loading icon
        if (state == 'running') {
            document.getElementById(`${item.id}_icon_offline`).setAttribute('hidden', '');
            document.getElementById(`${item.id}_icon_running`).removeAttribute('hidden');
            
        } else if (state == 'offline') {
            document.getElementById(`${item.id}_disabled_button`).setAttribute('hidden', '');
            document.getElementById(`${item.id}_start_button`).removeAttribute('hidden');
        } else {
            document.getElementById(`${item.id}_icon_offline`).setAttribute('hidden', '');
            document.getElementById(`${item.id}_icon_loading`).removeAttribute('hidden');
        }
    }
}

// start server, triggered by button press
// reloads page on completion to refresh statuses
async function start_server(element) {
    let server_id = element.getAttribute('value');

    console.log(`Sending start signal for ${server_id}`);
    document.getElementById(`${server_id}_icon_offline`).setAttribute('hidden', '');
    document.getElementById(`${server_id}_start_button`).setAttribute('hidden', '');
    document.getElementById(`${server_id}_icon_loading`).removeAttribute('hidden');
    document.getElementById(`${server_id}_disabled_button`).removeAttribute('hidden');

    try {
        let response = await fetch(`/start/${server_id}`, {method: "POST"});
        let status = await response.text();
        console.log("Success:", status);
    } catch (error) {
        console.error("Error:", error);
    }

    location.reload();
}


unhide_elements();
