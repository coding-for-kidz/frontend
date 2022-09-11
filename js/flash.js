function getNotifications() {
    fetch('/api/notifications/')
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.error('[Cache Updater ERROR] Server error while checking for updates, status code ' + response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {

                })
            })
}