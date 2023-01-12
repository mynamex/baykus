function dataURLtoFile(dataurl, filename) {

            var arr = dataurl.split(','),
                mime = arr[0].match(/:(.*?);/)[1],
                bstr = atob(arr[1]),
                n = bstr.length,
                u8arr = new Uint8Array(n);

            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }

            return new File([u8arr], filename, {type: mime});
        }

function imageResize(img,imageFile){
    let canvas = document.createElement("canvas"),
        context = canvas.getContext('2d'),
        originalWidth = img.width,
        originalHeight = img.height,
        mw = 500,
        mh = 500,
        rf = 1,
    quality = 0.8;

    canvas.width= mw;
    canvas.height=mh;

    context.drawImage(img,0,0, mw*rf, mh * rf);

    // Show resized image in preview element
    let dataurl = canvas.toDataURL(imageFile.type);
    return dataURLtoFile(dataurl, imageFile.name);
}