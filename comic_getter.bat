@if (@CodeSection == @Batch) @then

@echo off

setlocal


for %%i in (Mon,Tue,Wed,Thu,Fri,Sat) do (
    if "%date:~0,3%"=="%%i" goto YES
)

:NO
CScript //nologo //E:JScript "%~F0" > "daily_comics.html"
goto :EOF

:YES
CScript //nologo //E:JScript "%~F0" > "daily_comics.html"
goto :EOF

@end

var http = WScript.CreateObject('Msxml2.ServerXMLHTTP');

// Date setup
var today = new Date();
var dd = today.getDate();
var last_sunday = dd -  today.getDay();
var mm = today.getMonth()+1; //January is 0!
var yyyy = today.getFullYear();
if(dd<10) {
    dd = '0'+dd
}
if(last_sunday<10) {
    last_sunday = '0'+last_sunday
}
if(mm<10) {
    mm = '0'+mm
}
today = yyyy + '-' + mm + '-' + dd;


function comicsKingdom(url){
http.open("GET", url, false);
http.send();

if (http.status == 200) {
//var start = http.responseText.indexOf("cv-comic");
var url_start = http.responseText.indexOf("https://wp.comicskingdom.com/comicskingdom-redesign-uploads-production/");
var url_end = http.responseText.indexOf(".jpg", url_start);
WScript.Echo("<img src=\"https://comicskingdom.com/_next/image?url=" + http.responseText.substring(url_start, url_end) + ".jpg&w=1080&q=75\" width=\"100%\"></img>");
} else {
  WScript.StdOut.WriteLine("Error: Status "+http.status+" returned on download.");
}
}


function goComics(url){
http.open("GET", url, false);
http.send();

if (http.status == 200) {
var start = http.responseText.indexOf("item-comic-image");
var url_start = http.responseText.indexOf("src=", start) + 5;
var url_end = http.responseText.indexOf("\"", url_start);
WScript.Echo("<img src=\"" + http.responseText.substring(url_start, url_end) + "\" width=\"100%\"></img>");
} else {
  WScript.StdOut.WriteLine("Error: Status "+http.status+" returned on download.");
}
}


//////////////////////////////////////////
// GARFIELD
//////////////////////////////////////////
WScript.Echo("<br /><br /> Garfield <br />");
var url = "http://www.gocomics.com/garfield/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// SHERMANS LAGOON
//////////////////////////////////////////
WScript.Echo("<br /><br /> Sherman's Lagoon <br />");
var url = "http://www.gocomics.com/shermanslagoon/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// PICKLES
//////////////////////////////////////////
WScript.Echo("<br /><br /> Pickles <br />");
var url = "http://www.gocomics.com/pickles/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// GET FUZZY
//////////////////////////////////////////
WScript.Echo("<br /><br /> Get Fuzzy <br />");
var url = "http://www.gocomics.com/getfuzzy/" + yyyy + '/' + mm + '/' + dd;
goComics(url);
                     
//////////////////////////////////////////
// OVER THE HEDGE
//////////////////////////////////////////
WScript.Echo("<br /><br /> Over the Hedge <br />");
var url = "http://www.gocomics.com/overthehedge/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// CUL DE SAC
//////////////////////////////////////////
WScript.Echo("<br /><br /> Cul De Sac <br />");
var url = "http://www.gocomics.com/culdesac/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

// //////////////////////////////////////////
// // RETAIL
// //////////////////////////////////////////
// WScript.Echo("<br /><br /> Retail <br />");
// var url = "http://www.retailcomic.com";
// http.open("GET", url, false);
// http.send();
//
// if (http.status == 200) {
//     //var start = http.responseText.indexOf("cv-comic");
//     var url_start = http.responseText.indexOf("https://safr.kingfeatures");
//     var url_end = http.responseText.indexOf("\"", url_start);
//     WScript.Echo("<img src=\"" + http.responseText.substring(url_start, url_end) + "\"width=\"100%\"></img>");
// } else {
//    WScript.StdOut.WriteLine("Error: Status "+http.status+" returned on download.");
// }

//////////////////////////////////////////
// DEFLOCKED
//////////////////////////////////////////
WScript.Echo("<br /><br /> Deflocked <br />");
var url = "http://www.gocomics.com/deflocked/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// BC
//////////////////////////////////////////
WScript.Echo("<br /><br /> BC <br />");
var url = "http://www.gocomics.com/bc/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// CALVIN AND HOBBES
//////////////////////////////////////////
WScript.Echo("<br /><br /> Calvin and Hobbes <br />");
var url = "http://www.gocomics.com/calvinandhobbes/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Nonsequitor
//////////////////////////////////////////
WScript.Echo("<br /><br /> Nonsequitor <br />");
var url = "https://www.gocomics.com/nonsequitur/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Close to Home
//////////////////////////////////////////
WScript.Echo("<br /><br /> Close to Home <br />");
var url = "https://www.gocomics.com/closetohome/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Peanuts
//////////////////////////////////////////
WScript.Echo("<br /><br /> Peanuts <br />");
var url = "https://www.gocomics.com/peanuts/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Beetle Bailey
//////////////////////////////////////////
WScript.Echo("<br /><br /> Beetle Bailey <br />");

var url = "https://comicskingdom.com/beetle-bailey-1/" + yyyy + '-' + mm + '-' + dd;
comicsKingdom(url);

//////////////////////////////////////////
// Mutts
//////////////////////////////////////////
WScript.Echo("<br /><br /> Mutts <br />");

var url = "https://comicskingdom.com/mutts/" + yyyy + '-' + mm + '-' + dd;
comicsKingdom(url);

//////////////////////////////////////////
// Mother Goose and Grim
//////////////////////////////////////////
WScript.Echo("<br /><br /> Mother Goose and Grim <br />");
var url = "http://www.gocomics.com/mother-goose-and-grimm/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Wizard of ID
//////////////////////////////////////////
WScript.Echo("<br /><br /> Wizard of ID <br />");
var url = "http://www.gocomics.com/wizardofid/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Baldo
//////////////////////////////////////////
WScript.Echo("<br /><br /> Baldo <br />");
var url = "http://www.gocomics.com/baldo/" + yyyy + '/' + mm + '/' + dd;
goComics(url);

//////////////////////////////////////////
// Hi and Lois
//////////////////////////////////////////
WScript.Echo("<br /><br /> Hi and Lois <br />");

var url = "https://comicskingdom.com/hi-and-lois/" + yyyy + '-' + mm + '-' + dd;
comicsKingdom(url);

//////////////////////////////////////////
// Big Nate
//////////////////////////////////////////
WScript.Echo("<br /><br /> Big Nate <br />");
var url = "http://www.gocomics.com/bignate/" + yyyy + '/' + mm + '/' + dd;
goComics(url);