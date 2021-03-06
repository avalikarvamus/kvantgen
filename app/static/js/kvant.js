var paper = null
var aStar = null;

function initPaper() {
	if (paper) paper.remove();
	paper = Raphael(80, 80, 900, 600);
}

function loadStars() {
	$.getJSON("/api/stars.json", function (json) {
		console.log(json);
		//var arr = $.parseJSON(json);
		//$.each(json.allstars, function (star) {
			//console.log(arr);
			for (star in json.allstars) {
				console.log(star);
				console.log(star.name + " " + star.cx + " " + star.cy);
			}
		//});
	});
}

function loadStarXML(id) {
	$.ajax({
		type: "GET",
	url: "/api/star"+id+".xml",
	dataType: "xml",
	success: function(xml) {
		$('#sidebar').html("");
		$(xml).find('star').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			$('#sidebar').append("<br>Star: "+name+"<br>Coords: "+cx+":"+cy+"<br>Mass: "+mass);
		});
		$(xml).find('planets').find('planet').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			$('#sidebar').append("<br>Planet: "+name+"<br>Coords: "+cx+":"+cy+"<br>Mass: "+mass);
		});

	}
	});
}

function loadShipXML(id) {
	$.ajax({
		type: "GET",
	url: "/api/ship"+id+".xml",
	dataType: "xml",
	success: function(xml) {
		$(xml).find('star').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			var planets = "<br>";
			$(xml).find('planet').each(function(){
				planets = planets + "<br>" + $(this).find('name').text();
			});
			$('#sidebar').html("Star: "+name+"<br>Coords: "+cx+":"+cy+"<br>Mass: "+mass+"<br>"+planets);
		});
	}
	});
}

function loadStarsXML() {
	$.ajax({
		type: "GET",
	url: "/api/stars.xml",
	dataType: "xml",
	success: function(xml) {
		$(xml).find('star').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			//$('<div class="items" id="link_'+id+'"></div>').html('<a href="'+url+'">'+title+'</a>').appendTo('#page-wrap');
			console.log(name + "-" + cx + "-" + cy);
			var circle = paper.circle(cx*2.9, cy*1.9, 4);
			var color = "#f77";
			if (mass < 2000) { color = "#f88" } else
			if (mass < 4000) { color = "#f99" } else
			if (mass < 7000) { color = "#fbb" } else
			if (mass < 9000) { color = "#fcc" } else
			if (mass < 12000) { color = "#fdd" } else
			if (mass < 18000) { color = "#adf" } else
			if (mass < 22000) { color = "#aff" }
			circle.attr("fill", color);
			circle.attr("class","stars");
			circle.click(function () {
				if (aStar!= null) {
					aStar.remove();
				}
				aStar = paper.text(cx*2.9-5, cy*1.9+7, name).attr({fill: "#f00"}).node.setAttribute("class","track"); //ellipse(cx*2.9, cy*1.9, 13, 8); //popup(cx*2.9, cy*1.9, "Laev", "left", 1);
				loadStarXML(id);
				console.log("klikk");
			});
		});
	}
	});
}


function loadMapXML() {
	$.ajax({
		type: "GET",
	url: "/api/systems.xml",
	dataType: "xml",
	success: function(xml) {
		$(xml).find('system').each(function(){
			var star = $(this).find('star');
			var id = $(star).find('id').text();
			var name = $(star).find('name').text();
			var cx = $(star).find('cx').text();
			var cy = $(star).find('cy').text();
			var mass = $(star).find('mass').text();
			//$('<div class="items" id="link_'+id+'"></div>').html('<a href="'+url+'">'+title+'</a>').appendTo('#page-wrap');
			console.log(name + "-" + cx + "-" + cy);
			var circle = paper.circle(10+cx*4.2*2, 10+cy*2.9*2, 6);
			var color = "#f77";
			if (mass < 2000) { color = "#f88" } else
			if (mass < 4000) { color = "#f99" } else
			if (mass < 7000) { color = "#fbb" } else
			if (mass < 9000) { color = "#fcc" } else
			if (mass < 12000) { color = "#fdd" } else
			if (mass < 18000) { color = "#adf" } else
			if (mass < 22000) { color = "#aff" }
			circle.attr("fill", color);
			circle.attr("class","stars");
			circle.click(function () {
				if (aStar!= null) {
					aStar.remove();
				}
				aStar = paper.text(10+cx*8.4-5, 10+cy*5.8+7, name).attr({fill: "#f00"}).node.setAttribute("class","track"); //ellipse(cx*2.9, cy*1.9, 13, 8); //popup(cx*2.9, cy*1.9, "Laev", "left", 1);
				loadStarXML(id);
				console.log("klikk");
			});
			i = 1;
			$(this).find('planet').each(function(){
				//var planet = $(this).find('planet');
				var a, b = 0;
				if (i == 1) { a = -7; b = -2;}
				if (i == 2) { a = 3; b = -2;}
				if (i == 3) { a = -3; b = 4;}
				if (i == 4) { a = 7; b = 4;}
				if (i == 5) { a = -9;}
				var pmass = $(this).find('mass').text();
				var pcolor = "#777";
				var diag = 3;
				if (pmass < 11) { pcolor = "#388"; diag = 1 } else
				if (pmass < 12) { pcolor = "#399"; diag = 1 } else
				if (pmass < 14) { pcolor = "#3bb"; diag = 2 } else
				if (pmass < 15) { pcolor = "#3cc"; diag = 2 } else
				if (pmass < 16) { pcolor = "#3dd"; diag = 3 } else
				if (pmass < 18) { pcolor = "#3df"; diag = 3 } else
				if (pmass < 20) { pcolor = "#3ff"; diag = 4 }
				var planet = paper.circle(10+cx*8.4+a, 10+cy*5.8+b, diag);
				console.log(pmass);
				planet.attr("fill", pcolor);
				i++;
			});
		});
	}
	});
}

function loadShipsXML() {
	$.ajax({
		type: "GET",
	url: "/api/ships.xml",
	dataType: "xml",
	success: function(xml) {
		var i = 1;
		$(xml).find('ship').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			//$('<div class="items" id="link_'+id+'"></div>').html('<a href="'+url+'">'+title+'</a>').appendTo('#page-wrap');
			console.log(name + "-" + cx + "-" + cy);
			var circle = paper.circle(30, i*30, 20, 4);
			var color = "#f77";
			circle.attr("fill", color);
			var silt1 = paper.text(80, i*30, name).attr({fill: "#f00"});
			var silt2 = paper.text(180, i*30, mass).attr({fill: "#f00"});
			var silt3 = paper.text(240, i*30, mass).attr({fill: "#f00"});
			var ellip = paper.ellipse(37, i*30, 13, 8);
			//var popeye = paper.popup(i*230, 20, "Laev", "left", 1);
			i++;
		});
	}
	});
}

function loadImperiumXML() {
	$.ajax({
		type: "GET",
	url: "/api/imperium.xml",
	dataType: "xml",
	success: function(xml) {
		$(xml).find('ship').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('name').text();
			var cx = $(this).find('cx').text();
			var cy = $(this).find('cy').text();
			var mass = $(this).find('mass').text();
			//$('<div class="items" id="link_'+id+'"></div>').html('<a href="'+url+'">'+title+'</a>').appendTo('#page-wrap');
			console.log(name + "-" + cx + "-" + cy);
			dashed = {fill: "none", stroke: "#666", "stroke-dasharray": "- "};
			var circle1 = paper.ellipse(10+cx*8.4, 10+cy*5.8, 5, 3);
			var circle2 = paper.path("M10"+10+cx*8.4 + " " + 10+cy*5.8 +" "+ 4).attr(dashed); //circle(cx*2.9, cy*1.9, 4);
			var color = "#779";
			circle1.attr("fill", color);
			circle2.attr("fill", color);
			circle1.click(function () {
				console.log("klikk");
				aStar = paper.text(10+cx*8.4-5, 10+cy*5.8+7, name).attr({fill: "#f00"}); //ellipse(cx*2.9, cy*1.9, 13, 8); //popup(cx*2.9, cy*1.9, "Laev", "left", 1);
			});
		});
	}
	});
}

function loadLeadersJSON() {
	$.ajax({
		type: "GET",
	url: "/api/leaders.json",
	dataType: "jaon",
	success: function(json) {
		var i = 1;
		$(json).find('person').each(function(){
			var id = $(this).find('id').text();
			var name = $(this).find('firstname').text();
			var surename = $(this).find('surename').text();
			console.log(firstname + "-" + surename);
			var circle = paper.circle(30, i*30, 20, 4);
			var color = "#f77";
			circle.attr("fill", color);
			var silt1 = paper.text(80, i*30, name).attr({fill: "#f00"});
			var silt2 = paper.text(180, i*30, mass).attr({fill: "#f00"});
			var silt3 = paper.text(240, i*30, mass).attr({fill: "#f00"});
			var ellip = paper.ellipse(37, i*30, 13, 8);
			//var popeye = paper.popup(i*230, 20, "Laev", "left", 1);
			i++;
		});
	}
	});
}

function displayShips() {
	initPaper();
	var bot = paper.bottom, res = [];
	while (bot) {
		//res.push(bot);
		bot.hide();
		bot = bot.next;
	}
	loadShipsXML();
	$('#sidebar').empty();
	console.log("hidden ... suposed to be ...");
}

function displayStars() {
	initPaper();
	loadMapXML();
	loadImperiumXML();
	var bot = paper.bottom, res = [];
	while (bot) {
		//res.push(bot);
		bot.show();
		bot = bot.next;
	}
	$('#sidebar').empty();
	console.log("shown ... suposed to be ...");
}

function displayPlanets() {
	initPaper();
	loadMapXML();
	loadImperiumXML();
	var bot = paper.bottom, res = [];
	while (bot) {
		//res.push(bot);
		bot.show();
		bot = bot.next;
	}
	$('#sidebar').empty();
	console.log("shown ... suposed to be ...");
}

function displayLeaders() {
	initPaper();
	var bot = paper.bottom, res = [];
	while (bot) {
		//res.push(bot);
		bot.hide();
		bot = bot.next;
	}
	loadLeadersJSON();
	$('#sidebar').empty();
	console.log("hidden ... suposed to be ...");
}

$(document).ready(function()  {
	displayStars();
	//loadImperiumXML();
});
