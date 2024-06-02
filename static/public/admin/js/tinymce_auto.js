$(function(){
    const example_image_upload_handler = (blobInfo, progress) => new Promise((resolve, reject) => {
		const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		const xhr = new XMLHttpRequest();
		xhr.withCredentials = false;
		xhr.open('POST', '/manager/upload/upload_tinymce/');
		xhr.setRequestHeader('X-CSRFToken', csrftoken);
		xhr.upload.onprogress = (e) => {
			progress(e.loaded / e.total * 100);
		};

		xhr.onload = () => {
			if (xhr.status === 403) {
				reject({ message: 'HTTP Error: ' + xhr.status, remove: true });
				return;
			}

			if (xhr.status < 200 || xhr.status >= 300) {
				reject('HTTP Error: ' + xhr.status);
				return;
			}

			const json = JSON.parse(xhr.responseText);

			if (!json || typeof json.location != 'string') {
				reject('Invalid JSON: ' + xhr.responseText);
				return;
			}

			resolve(json.location);
		};

		xhr.onerror = () => {
			reject('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
		};

		const formData = new FormData();
		formData.append('file', blobInfo.blob(), blobInfo.filename());

		xhr.send(formData);
	});

	tinymce.init({
		selector: '.tinymce-textarea', //容器，可使用css选择器
		language:'zh_CN', //调用放在langs文件夹内的语言包
		plugins: "code image codesample preview",
		toolbar: [ //数组写法
			'code image codesample preview',
		],
		menubar: true, //隐藏菜单栏 
		convert_urls:false,
		promotion: false,
		branding: false,
		images_upload_handler: example_image_upload_handler
	});
});
