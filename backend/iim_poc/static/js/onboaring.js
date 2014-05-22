

        function formatDomain(item){
            if (item.id!=''){
                console.log('fs '); 
                console.log(item);
                var img= '<img class="flag" src="/static/img/domain_img/'+item.id.toLowerCase()+'Small.png"/>'
                return img+item.id;
            }
        }
        $("#domainList").select2({
           formatSelection: formatDomain,
           formatResult: formatDomain
        });

         function showPolicyConstraints(){
            console.log('func called');
        }

        function generateComponentContainerDiv(divClassName, labelText, listClassName, containerClassName, policyClassName){
            var subClassRow= $('<div class="row mwareapps" style="margin-top: 10px; background: rgba(12,45,66,0.5);"></div>');
            var subClassLabel= $('<div class="col-md-2"><h3> <span class="label label-success">Select Middlware Application</span></h3></div>');
            var subClassListContainer= $('<div class="col-md-8"></div>');
            var subClassList= $('<ul class="list-inline intro-social-buttons middleware-applications"></ul></div>');
        }

        function format(state) {
            console.log('the value coming in is ');
            console.log(state);
    if (!state.id) return state.text; // optgroup
    return '<img  data-toggle="tooltip" data-original-title="Click for application naming convention" data-placement="top" class="flag" src="/static/img/unchecked.png"/>' + state.text;
}
$("#source").select2({
    formatResult: format,
    formatSelection: format,
    placeholder: "Check Application Policy Compliance",
    allowClear: true,
    escapeMarkup: function(m) { return m; }
});
