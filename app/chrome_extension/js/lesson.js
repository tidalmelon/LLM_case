$("#openback").click(e => {
	window.open(chrome.extension.getURL("back.html"))
});

$("#getbacktitle").click(e => {
	var bg = chrome.extension.getBackgroundPage();
	alert(bg.document.title);
});

$("#setbacktitle").click(e => {
	var title = prompt("请输入后台页新标题", "新标题");
	var bg = chrome.extension.getBackgroundPage();
	bg.document.title = title;
	alert(bg.document.title);
});


$("#callbackjs").click(e => {
	// 获取了后台页对象
	var bg = chrome.extension.getBackgroundPage();
	// 执行后台页函数
	bg.backjs();
});