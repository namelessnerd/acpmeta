function getMiddlwareComponents(){
    $.ajax({
        url: "/get/middleware",
        dataType: 'json'
    })
    .done(function(data){
        $('#application-components').empty();
        $(document).data('middleware-type',{});
        $.each(data['middleware'], function(idx, val){
                var mwareHtml= $('<li id="'+ val[1].replace(/\s/g, '')+'"rel="'+val[0]+'"class="mware domain-icons" style="padding: 0.3em;margin-left: 0.4em;"/>');
                mwareHtml.append('<div><img src="/static/img/'+val[1].toLowerCase()+'.png"/></div>');
                mwareHtml.append('<div>'+val[1]+'</div>');
                $(document).data('middleware-type')[val[1].replace(/\s/g, '')]=[];
                $('#application-components').append(mwareHtml);
            });
            initMiddlwareClicks();        
    });// end ajax
}// end getMiddlewareComponents

// for each middleare, gets the associated applications and policies with it

function initMiddlwareClicks(){
    $('.mware').on({
        'click': function(){
            // check if the user has made any selections from this. if so
            // for now, do not reload. Desired is an alert check behavior
            // with option to keep those selected as long as they are in the
            //result.
            var current= $(this);
            var doc= $(document);
            var middlewareType= doc.data('middleware-type');
            console.log(middlewareType);
            if (doc.data('currentComponent')){
                doc.data('currentComponent').css({'background':'none'});
            }
            doc.data('currentComponent',current);
            var parent= current.attr('id');
            current.css({'background':'black'});
            // if (middlewareType && middlewareType.hasOwnProperty(parent) && middlewareType[parent].length>0){
            //     var selected= middlewareType[parent];
            //     for (var i= 0; i<selected.length; i++){
            //         alert('#'+selected[i]);
            //         $('#'+selected[i]).css({'background':'rgba(30,30,30,0.6)'});
            //     }
            // }

                // closure function to enable creation of application type
                // objects to be stored in local store. Takes in the AJAX
                // response from server
                var createApplicationType= function(data){
                     if (data['subClasses']){
                        $('#application-list').empty();
                        doc.data('middlware-apps', {});
                        $.each(data['subClasses'], function(idx, val){
                            var appId= val[1].replace(/\s/g, '');
                            var mwareHtml= $('<li id="'+appId+'" rel="'+val[0]+'"class="mwareApps domain-icons" style="padding: 0.3em;margin-left: 0.4em;"/>');
                            mwareHtml.append('<div><img src="/static/img/appComponents/'+val[1].toLowerCase()+'.png"/></div>');
                            mwareHtml.append('<div>'+val[1]+'</div>');
                            doc.data('middlware-apps')[appId]= {'uri':val[0], 
                                            'parent':parent, 
                                            'selected':0};
                            if (middlewareType && middlewareType.hasOwnProperty(parent) && middlewareType[parent].length>0){
                                if (middlewareType[parent].indexOf(appId)!=-1)
                                    mwareHtml.css({'background':'rgba(30,30,30,0.6)'});
                            }
                            // doc.data('middleware-type')[parent].push(val[1].replace(/\s/g, '');
                            $('#application-list').append(mwareHtml);


                        });
                        initMiddlewareAppClick();
                    }
                }

                var processPolicyForMiddleware= function(data){
                    $('.app-component-policies').empty();
                    $.each(data, function(idx, val){
                        var policyID= val['name'].replace(/\s/g, '');
                        var policy= $('<button id="'+ policyID +'" rel="'+ val['uri']+'" class=" btn-danger"></button>)" ');
                        policy.append('<h5>'+val['name']+'</h5>');
                        $('.app-component-policies').append(policy);
                    }); // end for each data
                }// end process policy for Middleware

                $.ajax({
                    url: "/get/subClass",
                    data:{"parentClass":$(this).attr('rel')},
                    dataType: 'json'
                })
                .done(createApplicationType);

                // get the associted policy with it
                $.ajax({
                    url: "/get/policy",
                    data:{"middleware":$(this).attr('rel')},
                    dataType: 'json'
                })
                .done(processPolicyForMiddleware);


        }// end function for click 
    }); // end on params
}// end function
                           
        function initMiddlewareAppClick() {
            console.log('function called');

             $('.mwareApps').on({
                                    'click': function(){
                                        var current= $(this);
                                        var doc= $(document);
                                        current.css({'background':'black'});
                                        var appObj= doc.data('middlware-apps')[current.attr('id')];
                                        var parent= appObj['parent'];
                                        console.log(doc.data('middleware-type'));
                                        doc.data('middleware-type')[parent].push(current.attr('id'));
                                        console.log(doc.data('middleware-type'));
                                        $('#'+$(this).attr('id')+'-pol').css({"display":"block"});

                                        

                                        $('.polcomp').on({
                                            'click': function(){
                                                alert('clicked');
                                                $("#policyChecklist").select2("val", "http://ontology.techlabs.acn.com/policyModel#SecurityPolicy");
                                                $("#policyChecklist").select2({'placeholder':"Checklist for "+ $('#appType').html() +" application in " + $('#appDomain').html(),
                                                            formatResult: formatPolicy,
                                                            formatSelection: formatPolicySelection,
                                                             allowClear: true
                                                        });
                                            }
                                        })
                                        // $.ajax({
                                        //     url: "get/policy/components",
                                        //     // This call currently handles only one policy requirement. The code must change to iterate over 
                                        //     // all policies in the stack and then show the results accordingly. this must be either in code or 
                                        //     // the request must be a json with the iteration handled in server.
                                        //     data:{"component":$(this).attr('rel'), "policyModule":$(document).data('policy')[0]},
                                        //     dataType: 'json'
                                        // })
                                        // .done(function(data){
                                        //     console.log(data);
                                        //     $.each(data['policyModule'], function(idx, val){
                                        //         var pol_req='<li><h4><span class="label label-danger">'+val[1]+'</span></h4></li>';
                                        //         $('.pol-comp').append(pol_req);
                                        //     });
                                        // });
                                    }       

                                });
        }

