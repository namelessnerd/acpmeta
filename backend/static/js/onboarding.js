function formatDomain(item){
    if (item.id!=''){
        var img= '<img class="flag" src="/static/img/domain_img/'+item.id.toLowerCase()+'Small.png"/>'
        return img+item.id;
    }
}
$("#domainList").select2({
   formatSelection: formatDomain,
   formatResult: formatDomain
});

$("#appTypeList").select2();

 function showPolicyConstraints(){
    console.log('func called');
}

function generateComponentContainerDiv(divClassName, labelText, listClassName, containerClassName, policyClassName){
    var subClassRow= $('<div class="row mwareapps" style="margin-top: 10px; background: rgba(12,45,66,0.5);"></div>');
    var subClassLabel= $('<div class="col-md-2"><h3> <span class="label label-success">Select Middlware Application</span></h3></div>');
    var subClassListContainer= $('<div class="col-md-8"></div>');
    var subClassList= $('<ul class="list-inline intro-social-buttons middleware-applications"></ul></div>');
}

function formatPolicy(state) {
    console.log($(document).data('fulfilled'));
    console.log(state.id);
    // console.log($(document).data('fulfilled') && $(document).data('fulfilled').indexOf(state.id));
    // console.log($(document).data('fulfilled').indexOf(state.id));
    if (!state.id) return state.text; // optgroup
    if ($(document).data('fulfilled') && $(document).data('fulfilled').indexOf(state.id)!=-1){
        console.log('Matching element is ' + state.id);
        return '<img id='+state.id+' src="/static/img/checked1.png"/>' + state.text;
    }
    else 
        return '<img id='+state.id+' src="/static/img/unchecked.png"/>' + state.text;
}

function formatPolicySelection(state) {
    var fulfilledPolicy= $(document).data('fulfilled') ? $(document).data('fulfilled') : [];
    fulfilledPolicy.push(state.id);
    console.log(fulfilledPolicy);
    $(document).data('fulfilled', fulfilledPolicy);
    if (!state.id) return state.text; // optgroup
        return '<img src="/static/img/checked1.png"/>' + state.text;
    
}

$("#policyChecklist").select2({
    formatResult: formatPolicy,
    formatSelection: formatPolicySelection,
    placeholder: "Choose Application domain and type to load policy checklist"
});
$("#policyChecklist").click(function () { alert("Selected value is: "+$("#policyChecklist").select2("val"));});