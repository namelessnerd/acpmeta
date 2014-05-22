// sets the application domain
$('#domainList').change(function() {
	var doc= $(document);

	if (!(doc.data('appName'))){
		var appDomain= $('#domainList option:selected').text();
		$('#appDomain').html($(this).val());
		$(document).data('appDomainURI', appDomain);
		$(document).data('appDomainName', $(this).val());
		// get application types for this domain
		$.ajax({
                url: "/get/apptype",
                data:{'domain':appDomain},
                dataType: 'json'
            })
            .done(function(data){
                for (var record in data) {
                    $('#appTypeList').append("<option value=\""+data[record]['uri']+"\">"+data[record]['name']+"</option>") ;
                }
            });
	}
	else {
		alert('You already have created an application. Changing the domain will remove all configurations.')
	}
});


$('#appTypeList').change(function() {
	var doc= $(document);
	if (!(doc.data('appType'))){
		var appType= $('#appTypeList option:selected').text();
		$('#appType').html(appType);
		$('.app-name').prop('disabled',false);
		$(document).data('appType', $(this).val());

		// load the policy checklist
		$.ajax({
      url: "/get/policy",
      data:{'domain':$(document).data('appDomainURI'), 'appType':$(this).val()},
      dataType: 'json'
    })
    .done(function(data){
			// var policyContainer= $('#policyChecklist');
			// var webServerGroup= $('<optgroup label="Web Server">');
			// webServerGroup.append('<option value="AK">Security Policy</option>');
			// policyContainer.append(webServerGroup);
			// policyContainer.append('<option value="HI">Authentication Policy</option>');
			var policyContainer= $('#policyChecklist');
      var webServerGroup;
      for (var record in data) {
        webServerGroup= $('<optgroup label="'+data[record]['name']+'"/>');
        var policies= data[record]['policies'];
        for (var policy in policies){
          webServerGroup.append('<option value="'+policies[policy]['uri']+'">'+policies[policy]['name']+'</option>');}
        policyContainer.append(webServerGroup);
        console.log(policyContainer);
      }
      policyContainer.select2({'placeholder':"Checklist for "+ $('#appType').html() +" application in " + $('#appDomain').html(),
    														formatResult: formatPolicy,
    														formatSelection: formatPolicySelection,
    														 allowClear: true
    													});
     	
		});



		// policyContainer.append(webServerGroup);
		// policyContainer.select2({
  //   	formatResult: formatPolicy,
  //   	formatSelection: formatPolicySelection,
  //   	placeholder: "Checklist for "+ $('#appType').html() +" application in " + $('#appDomain').html(),
  //   	allowClear: true,
  //   	escapeMarkup: function(m) { return m; }
		// });
		// policyContainer.select2("val", "AK"); 
		
		// policyContainer.on("change", function(e) { 
  //   		console.log("change "+ e.val); 
  //   	});

                   
                   
               // </optgroup>
               // <optgroup label="Database Server">
               //     <option value="CA">Storage Policy</option>
               //     <option value="NV">Authentication Policy</option>
               // </optgroup>


	}
	else {
		alert('You already have chosen an Application Type. Changing the domain will remove all configurations.')
	}
});




$('.app-save').on('click', function(){
	var reg = /^[A-Za-z\d]+$/;
	var val= $('.app-name').val();
	var doc= $(document);
	if (reg.test(val))
		{
			var name= doc.data('appDomainName').toLowerCase()+'_'+val;
			doc.data('appName', doc.name);
			$('#appName').html(name);
			getMiddlwareComponents();
			
		}
	else 
		alert('Invalid name');	
});

$(function () { $("[data-toggle='popover']").popover({'trigger':'hover'}); });
