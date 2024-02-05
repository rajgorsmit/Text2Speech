document.querySelector('#options').addEventListener('click', function() {
    if (chrome.runtime.openOptionsPage) {
        chrome.runtime.openOptionsPage();
    } else {
        window.open(chrome.runtime.getURL('options.html'));
    }
});

document.querySelector('#help').addEventListener('click', function() {
    if (chrome.runtime.openHelpPage) {
        chrome.runtime.openHelpPage();
    } else {
        window.open(chrome.runtime.getURL('help.html'));
    }
});

document.querySelector('#about').addEventListener('click', function() {
  if (chrome.runtime.openAboutPage) {  
      chrome.runtime.openAboutPage();
  } else {
      window.open(chrome.runtime.getURL('about.html'));
  }
});

document.querySelector('#info').addEventListener('click', function() {
    window.open('https://github.com/sparkled77/Text2Speech-Chrome-Extension/');
});

document.querySelector('#ourGithub').addEventListener('click', function() {
    window.open('https://github.com/sparkled77/Text2Speech-Chrome-Extension/'); 
});
var id = 0;
