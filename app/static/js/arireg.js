function compSearch() {
    $('#search').empty();
    $('#search').append('<div id="cmpsr">Ettevõtete otsing</div>');
    $('#search').append('<input id="searchinput" type="text" placeholder="firma nime osa või registrikood" autofocus required>');
    $('#search').append('<a href="javascript:searchCompany(1);" id="compsrs" class="btm">Otsi</a>');
    $('#search').append('<a href="javascript:ownSearch();" id="swsrs" class="btm">Vaheta</a>');
}

function ownSearch() {
    $('#search').empty();
    $('#search').prepend('<div id="ownsr">Ettevõtete omanike otsing</div>');
    $('#search').append('<input id="searchinput" type="text" placeholder="omaniku (pere)nime osa või registrikood" autofocus required>');
    $('#search').append('<a href="javascript:searchOwner(1);" id="ownersrs" class="btm">Otsi</a>');
    $('#search').append('<a href="javascript:compSearch();" id="swsrs" class="btm">Vaheta</a>');
}

function loadFirst() {
   $('#list').empty();
   compSearch();
   /*$("#message").empty();*/
   $('#compmaker').empty();
   $('#compmaker').append('<a href="javascript:loadAddCompany();" id="compmk" class="bt">Osaühingu asutamine</a>');
   $('#compmk').attr('class', 'bt');
   $('#list').append("Teretulemast Äriregistrisse!");
   $('#list').append("<p>Ülalt vasakult saate otsida ettevõtteid nende nimeosade ja registrinumbrite järgi.</p>");
   $('#list').append("<p>Nupust 'Vaheta' võite lülituda osanike otsingu režiimi, kus leiate ettevõtete omanikke.</p>");
   $('#list').append("<p>Ülalt paremalt saate minna ettevõtte loomise ekraanile.</p>");
   $('#list').append("<p>Tühjal ribal üleval kuvatakse erinevaid teateid õnnestunud ja ebaõnnestunud operatsioonidest.</p>");
}

function viga(teade) {
    $("#message").append("<div class='viga'>"+teade+"</div>");
}

function loadAddCompany() {
   $("#list").empty();
   $("#message").empty();
   $("#list").load("/add-company");
   if ($("#frontPg").length==0) $("#compmaker").append("<a href='/' class='bt' id='frontPg'>Esilehele</a>");
}

function loadCompany(cid) {
   $("#list").empty();
   /*$("#message").empty(); */  /* Et peale firma lisamist ka viimane teade nähtav oleks.*/
   $("#list").load("/comp/"+cid);
}

function showCompanyList(i) {
    $("#list").empty();
    $("#list").load("/complist/"+i);
}

function searchCompany(i) {
    $("#list").empty();
    if ($('#searchinput').val()) $("#list").load("/search/"+$('#searchinput').val()+"/"+i);
    else showCompanyList(i);
}

function showOwnerList(i) {
    $("#list").empty();
    $("#list").load("/ownerlist/"+i);
}

function searchOwner(i) {
    $("#list").empty();
    if ($('#searchinput').val()) $("#list").load("/ownsearch/"+$('#searchinput').val()+"/"+i);
    else showOwnerList(i);
}

function addOwnerRows() {
    number=$('#owner_number').val();
    $("#message").empty();
    if (isNaN(number) || number<1) {
        viga("Lisatavate osanike arv pole number või on alla ühe.");
	}
    else {
        $("#ownertable").empty();
        for (var i=0;i < number ;i++)
            {
                ///console.log("lisame rida "+i);
                ///$("<span id='own"+i+1+"></span>").appendTo("#ownertable");
                var ownname='<input id="owner_name'+(i+1)+'" name="ownername'+(i+1)+'" type="text" placeholder="'+(i+1)+'. osaniku nimi/perenimi" required>';
                var ownfirstname='<input id="owner_firstname'+(i+1)+'" name="ownerfirstname'+(i+1)+'" type="text" placeholder="füüsilisest isikust osaniku eesnimi">';
                var ownequ='<input id="owner_equity'+(i+1)+'" name="ownerequity'+(i+1)+'" type="text" placeholder="täisarvuline osalus" required>';
                var ownreg='<input id="owner_reg'+(i+1)+'" name="ownerreg'+(i+1)+'" type="text" placeholder="osaniku registrikood/isikukood" required>';
                var breaker='<br>';
                $("#ownertable").append(ownname,ownfirstname,ownequ,ownreg,breaker);
            }
        if ($("#postComp").length==0) $("#konfig").append('<a href="javascript:postData();" class="bt" id="postComp">Lisa osaühing</a>');
    }
}

function postData() {
  chkname = $('#company_name').val();
  equity = $('#company_equitycap').val();
  chkregnum = $('#company_regnum').val();
  chkmkdate = $('#company_date').val();
  chkequity = parseInt(equity);
  number=$('#owner_number').val();
  var owners = [];
  for (var i=0;i < number ;i++) {
      owners[i] = new Object();
      owners[i].owner_name=$('#owner_name'+(i+1)).val();
      owners[i].owner_firstname=$('#owner_firstname'+(i+1)).val();
      owners[i].owner_reg=$('#owner_reg'+(i+1)).val();
      owners[i].owner_equity=$('#owner_equity'+(i+1)).val();
      //owners[i].owner_name=$('#owner_name'+(i+1)).val();
    }
  var owners_to_send = JSON.stringify(owners);
  $("#message").empty();
  if (isNaN(chkequity) || chkequity<2500) {
	  viga("Kapital pole number või on väiksem kui 2500 €");
	}
  if (isNaN(chkregnum) || chkregnum<1000000 || chkregnum>9999999) {
	viga("Registrinumber pole number või on suurem või väiksem kui 7 kohta");
	} 
  if (chkname.toLowerCase().indexOf("oü") == -1 && chkname.toLowerCase().indexOf("osaühing") == -1) {
	viga("Nimi ei sisalda väljendeid OÜ ega Osaühing");
	}
  if (chkname.length < 3  || chkname.length > 100) {
	viga("Nimi ei ole üle kolme ja alla 100 märgi pikk");
    console.log(chkname.length);
	}
  /* TODO: Siia võiks lisada osanike nimede ja registrinumbrite/isikukoodide kontrollid */
  if ($(".viga").length==0) {
	$.post("/add-company", { compname: chkname, equitycap : equity, regnum :chkregnum, mkdate:chkmkdate, "owners" : owners_to_send }).done(function(data) {
        if (isNaN(data)) {
            viga("Midagi läks nihu, serveri teade kuvatakse all");
            $("#list").html(data);
        }
        else {
           $("#message").html("Firma lisati!");
           loadCompany(data);
        }
    });
	}
}

$(document).ready(function()  {
    loadFirst();
});  

$('bt').click(function()  {
	$(this).attr('class', 'abt');
	return false;		
  }
);
