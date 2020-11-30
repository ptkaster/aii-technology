var tabHTML = "";

document.addEventListener('DOMContentLoaded', function() {
  var checkPageButton = document.getElementById('checkPage');
  checkPageButton.addEventListener('click', function() {
    console.log("clicked");

    chrome.tabs.getSelected(null, function(tab) {
      d = document;

      var html = tabHTML;

      console.log(tab.url);


      params = {
        "html_body" : html
      }

      console.log(params)

      const Http = new XMLHttpRequest();
      const url='https://www.annenberginclusioninitiative.org/get_linkedin_csv';
      Http.open("POST", url);
      Http.setRequestHeader("Content-Type", "text/html");
      Http.send(JSON.stringify(params));
      console.log(url)
      var blob_object;
      var download_count = 0;

      var download_filename = String(tab.url).split("/")[4] + ".csv"

      Http.onreadystatechange = (e) => {
        download_count += 1;
        // console.log(Http.responseText);
        csv = String(Http.responseText).split("\n");
        console.log(csv)
        var blob = new Blob([Http.responseText], {type: "text/csv"});
        blob_object = URL.createObjectURL(blob);
        if(download_count == 3){
          chrome.downloads.download({
            url: blob_object,
            filename: download_filename
          });
        }


        // document.getElementById('response').innerHTML = Http.responseText;
      }



      // console.log(d);
      //
      // var f = d.createElement('form');
      // f.action = 'http://gtmetrix.com/analyze.html?bm';
      // f.method = 'post';
      // var i = d.createElement('input');
      // i.type = 'hidden';
      // i.name = 'url';
      // i.value = tab.url;
      // f.appendChild(i);
      // d.body.appendChild(f);
      // f.submit();
    });
  }, false);
}, false);


chrome.runtime.onMessage.addListener(function(request, sender) {
  if (request.action == "getSource") {
    message.innerText = request.source;
    tabHTML = request.source;
  }
});

function onWindowLoad() {

  var message = document.querySelector('#message');

  chrome.tabs.executeScript(null, {
    file: "getPagesSource.js"
  }, function() {
    // If you try and inject into an extensions page or the webstore/NTP you'll get an error
    if (chrome.runtime.lastError) {
      message.innerText = 'There was an error injecting script : \n' + chrome.runtime.lastError.message;
    }
  });

}

window.onload = onWindowLoad;
