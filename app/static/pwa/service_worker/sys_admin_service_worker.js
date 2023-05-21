// install service worker
const staticCacheName = 'v7dfgfdg5';
const assets = [
    // '/',
    // '/school',
    '/favicon.ico',
    // '/socket_worker.js',
    '/static/custom/js/jquery_charts.js',
    '/static/custom/js/jquery_forms.js',
    '/static/custom/js/jquery_ui.js',
    '/static/custom/css/main.css',
    // '/static/custom/js/main.js',
    '/static/custom/js/plugins.js',
    '/static/libs/bootstrap-5.2.2-dist/css/bootstrap.min.css',
    '/static/libs/bootstrap-5.2.2-dist/js/bootstrap.min.js',
    '/static/libs/font-awesome-4.7.0/css/font-awesome.min.css',
    '/static/libs/jquery/jquery-3.5.1.min.js',
    '/static/libs/socketio/socket.io.min.js',
    // '/static/pwa/app.js',
    '/static/pwa/icons/maskable_icon_x192.png',
    '/static/temp/css/animate.min.css',
    '/static/temp/css/bootstrap-icons.min.css',
    '/static/temp/css/datepicker.min.css',
    '/static/temp/css/all.min.css',
    '/static/temp/fonts/flaticon.css',
    '/static/temp/fonts/Flaticon.woff2',
    '/static/temp/js/datepicker.min.js',
    '/static/temp/js/fileinput.min.js',
    '/static/temp/js/intlTelInput.min.js',
    '/static/temp/js/jquery.scrollUp.min.js',
    '/static/temp/js/modernizr-3.6.0.min.js',
    '/static/temp/js/popper.min.js',
    '/static/temp/js/plugins.js',
    '/static/temp/js/select2.min.js',
    '/static/temp/webfonts/fa-regular-400.woff2',
    '/static/temp/webfonts/fa-solid-900.woff2',
    // 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/intlTelInput.min.js',
    // 'https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.5/js/fileinput.min.js',
    // 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/css/intlTelInput.css',
    // 'https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.5/css/fileinput.min.css',
    // 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.min.css'
];

self.addEventListener('install', evt => {
    evt.waitUntil(
        caches.open(staticCacheName).then(cache => {
            return cache.addAll(assets)
        }).then(self.skipWaiting()).catch(err => {
            console.log(err)
        })
    )
});

// activate service worker
self.addEventListener('activate', evt => {
    evt.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.filter(
                    key => key !== staticCacheName
                ).map(key => caches.delete(key))
            )
        })
    )
});

// fetch event
self.addEventListener('fetch', evt => {
    // console.log('fetch event', evt);
    evt.respondWith(
        caches.match(evt.request).then(cacheRes => {
            // console.log('cache response ', cacheRes);
            return cacheRes || fetch(evt.request);
        }).catch(err => console.error(err))
    );
});


self.addEventListener('push', function(event){
    console.log('Received push');
    let notificationTitle = 'Notification from server';
    let notificationOptions = {
        body: 'Server sent notification',
        tag: 'python-webnoti',
        // More options can be found at:
        // https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification
    };

    if (event.data){
        // Server sent you a data!
        notificationOptions.body = event.data.text();
    }
    if (event.tag){
        notificationOptions.tag = event.tag.text()
    }

    event.waitUntil(
        self.registration.showNotification(notificationTitle, notificationOptions)
    )
});

// console.log('Hello from sw.js');

// importScripts('https://storage.googleapis.com/workbox-cdn/releases/3.2.0/workbox-sw.js');

// if (workbox){
//     console.log(`Yay! Workbox is loaded 🎉`);

//     workbox.precaching.precacheAndRoute([
//         {
//             "url": "/",
//             "revision": "1"
//         }
//     ]);

//     workbox.routing.registerRoute(
//         /\.(?:js|css)$/,
//         workbox.strategies.staleWhileRevalidate({
//             cacheName: 'static-resources',
//         }),
//     );

//     workbox.routing.registerRoute(
//         /\.(?:png|gif|jpg|jpeg|svg)$/,
//         workbox.strategies.cacheFirst({
//             cacheName: 'images',
//             plugins: [
//                 new workbox.expiration.Plugin({
//                     maxEntries: 60,
//                     maxAgeSeconds: 30 * 24 * 60 * 60, // 30 Days
//                 }),
//             ],
//         }),
//     );

//     workbox.routing.registerRoute(
//         new RegExp('https://fonts.(?:googleapis|gstatic).com/(.*)'),
//         workbox.strategies.cacheFirst({
//             cacheName: 'googleapis',
//             plugins: [
//                 new workbox.expiration.Plugin({
//                     maxEntries: 30,
//                 }),
//             ],
//         }),
//     );
// } else {
//     console.log(`Boo! Workbox didn't load 😬`);
// };

// self.addEventListener('push', function(event){
//     console.log('Received push');
//     let notification = event.data;
//     let notificationTitle = 'Notification from server';
//     let notificationOptions = {
//         body: notification ? notification.text(): 'Server sent notification',
//         tag: 'python-webnoti',
//         // More options can be found at:
//         // https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification
//     };

//     if (event.data){
//         // Server sent you a data!
//         notificationOptions.body = event.data.text();
//     }

//     event.waitUntil(
//         self.registration.showNotification(
//             notificationTitle, notificationOptions)
//     )
// });
