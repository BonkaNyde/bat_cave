function showNotification(title, body='', icon='/favicon.ico', vibrate=true, click_visit_url='') {
    `A function to process notification rendering.`
    const notificationError = (error) => {
        console.error('notification error', error);
    };

    // check if app has notification permission granted.
    if (Notification.permission === 'granted') {
        const notification = new Notification(title, {
            icon: icon,
            body: body,
            renotify: true,
            vibrate: vibrate
        });
        notification.onerror = notificationError(error);
        if (click_visit_url) {
            notification.addEventListener('click', () => {
                window.open(click_visit_url, '_blank');
            });
        };

        // show notification popup for 10 seconds.
        setTimeout(() => {
            notification.close();
        }, 10 * 1000);
    };
};


$().ready(function () {
    // remove preloader from page
    $("#preloader").fadeOut("slow", function () {
        $(this).remove();
    });     
});
