function backjs()
{
	chrome.tabs.getSelected(null, function(tab){
		var title = tab.title
		chrome.tabs.executeScript(null, {code: "javascript: alert('" + title + "')"});
	});
}