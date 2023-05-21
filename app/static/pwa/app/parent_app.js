// const myWorker = new SharedWorker('/socket_worker.js');

const sockHandler = (host=window.location.hostname, port=location.port, namespace='')=>{
    let soc_scheme =  window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    var base_url = soc_scheme + '//' + host + (port ? `:${port}` : '');
    return io.connect(base_url + (namespace ? `/${namespace}` : ''), {
		transports: ["websocket", "polling"]
	});
};

const socket_io = sockHandler();

// const sendToWorker = (event, data, action="send") => {
//     console.log('sending message to worker', data);
//     let payload = JSON.stringify({
//         "event":event,
//         "data": data,
//         "action": action
//     });
//     myWorker.port.postMessage(payload);
// };

// window.addEventListener('beforeunload', function(e){
// 	let data = {
// 		description: 'unloading user port'
// 	};
//     sendToWorker(JSON.stringify(data), action='unload');
//     myWorker.port.close();
// });

function base64UrlToUint8Array(base64UrlData) {
    const padding = '='.repeat((4 - base64UrlData.length % 4) % 4);
    const base64 = (base64UrlData + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const buffer = new Uint8Array(rawData.length);

    for (let i = 0; i<rawData.length; ++i) {
        buffer[i] = rawData.charCodeAt(i);
    };
    return buffer;
};

// Check if PushManager is supported.
if('PushManager' in window){
	// If PushManager is supported, and push_service is enabled and
	// there is no active push subscription, create a push subscription. 
	console.log('push in window');
	const notification_permission = Notification.permission;
	if (notification_permission!=='granted' && notification_permission!=='denied'){
		navigator.serviceWorker.ready.then(registration => {
			socket_io.emit('get_perm', perm => {
				console.log(perm);
				const push_options = {
					userVisibleOnly: true,
					applicationServerKey: base64UrlToUint8Array(perm),
				};
				console.log(push_options);
				let push_enabled = registration.pushManager.getSubscription(push_options);
				if(push_enabled){
					registration.pushManager.subscribe(push_options).then(subscription=>{
						console.log('push subscription', subscription);
						socket_io.emit('push_notification_sub', JSON.stringify(subscription), function(data){
							console.log(data);
						});
						return subscription;
					}).catch(error => console.info(error));
				};
			});
		});
	};
};

window.addEventListener('load', ()=>{
	if ('serviceWorker' in navigator){
		// let element = document.getElementsByName('body')[0]
		// element.append(btnInstall)
		// register ServiceWorker
		// let sw_reg = navigator.serviceWorker.getRegistration();
		let service_worker_registration = navigator.serviceWorker.register('/parent/service_worker.js')
			.then(function (registration){
				console.log('Service Worker Registered', registration);
				return registration;
			});
		service_worker_registration.catch(function (err) {
			console.log('Unable to register service worker.', err);
		});
		// registerPushService()

		// const notification_perm = Notification.permission;
		
		// if(notification_perm === "granted"){
		// 	registerPushService();
		// }else if(notification_perm === "default"){
		// 	askNotificationPermission() === "granted" ? registerPushService() : console.warn('Notification permission denied.');
		// };
	};
});




// if('serviceWorker' in navigator){
//     let service_worker =  navigator.serviceWorker.register('/school/service_worker.js');
//     service_worker.then( reg => {
//         console.log('service worker registered', reg);
// 		return reg
//     }).catch( err => {
//         console.log('service worker not registered', err);
//     });
// };

navigator.serviceWorker.ready.then(function(reg){
	let deferredPrompt;
	const btnInstall = document.createElement('button');
	btnInstall.id = 'btnInstall';
	btnInstall.innerText = 'Install';
	btnInstall.style.visibility = 'hidden';
	console.log('registered scope: ', reg.scope);
	window.addEventListener('beforeinstallprompt', (e) => {
		console.log('beforeinstallprompt event fired');
		// document.body.append(btnInstall);
		e.preventDefault();
		deferredPrompt = e;
		btnInstall.style.visibility = 'visible';
	});
	
	btnInstall.addEventListener('click', (e) => {
		btnInstall.style.visibility = 'hidden';
		deferredPrompt.prompt();
		deferredPrompt.userChoice.then(choiceResult => {
			if (choiceResult.outcome === 'accepted') {
				console.log('User accepted the A2HS prompt');
			} else {
				console.log('User dismissed the A2HS prompt');
			};
			deferredPrompt = null;
		});
	});
});


window.addEventListener('appinstalled', evt=>{
	app.logEvent('app', evt);
});

// if ('BackgroundFetchManager' in self) {
//     // This browser supports Background Fetch!
//     navigator.serviceWorker.ready.then(
//         async (swReg) => {
//             const bgFetch = await swReg.backgroundFetch.fetch( 'my-fetch', ['/ep-5.mp3', 'ep-5-artwork.jpg'], {
//                 title: 'Episode 5: Interesting things.',
//                 icons: [
//                     {
//                         sizes: '300x300',
//                         src: '/ep-5-icon.png',
//                         type: 'image/png',
//                     }
//                 ],
//                 downloadTotal: 60 * 1024 * 1024,
//             });
//             bgFetch.addEventListener('progress', () => {
//                 // If we didn't provide a total, we can't provide a %.
//                 if (!bgFetch.downloadTotal) return;
//                 const percent = Math.round(bgFetch.downloaded / bgFetch.downloadTotal * 100);
//                 console.log(`Download progress: ${percent}%`);
//             });
//         }
//     );
// }

