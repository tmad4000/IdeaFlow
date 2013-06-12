lib('home', {

    init: function() {
        $('#idea-form').submit(function() {
            lib('ideas').add();
            return false;
        });
        lib('ideas').events();
        this.autocompletion();
        this.explorableTags();

       // $('body').on('click','span.label',function() {alert('a')})
        
//        this.color_ideas();
    },
    
    autocompletion: function() {
        // console.log('autocompletion test')

        // $('#idea-txt-2').keyup(function() {
        //     $('#ms-input-0').val($('#idea-txt-2').val());
        //     $('#ms-input-0').trigger('keyup');
        // });
        
        // var jsonData = [];
        // var cities = 'New York,Los Angeles,Chicago,Houston,Paris,Marseille,Toulouse,Lyon,Bordeaux,Philadelphia,Phoenix,San Antonio,San Diego,Dallas,San Jose,Jacksonville'.split(',');

        // for(var i=0;i<cities.length;i++) {
        //     jsonData.push(
        //         {
        //             id:i,
        //             name:cities[i],
        //             status:i%2?'Already Visited':'Planned for visit',
        //             coolness:Math.floor(Math.random() * 10) + 1
        //         });
        // }

        // console.log(jsonData)

        // $('#idea-txt-1').magicSuggest({
        //     selectionPosition: 'right',
        //     renderer: function(city){
        //         console.log('render city')
        //         console.log(city)            
        //         return '<div>' +
        //                 '<div style="font-family: Arial; font-weight: bold">' + city.name + '</div>' +
        //                 '<div><b>Cooooolness</b>: ' + city.coolness + '</div>' +
        //                '</div>';
        //     },
        //     minChars: 1,
        //     selectionStacked: true,
        //     data: jsonData
        // }); 

 //       var jsonData2 = [];

//        $.getJSON('/ajax/autocomplete/?autocomplete=', function(xdata) {

            //console.log('ajax read')
            //console.log(xdata);
            // jsonData2 = xdata;
/*
            $.each(xdata, function(key, val) {
                //console.log(val)


                jsonData2.push(
                    {
                        id : val.id,
                        name : val.title,
                        status : 'some status',
                        coolness : val.text
                    });
            });    
*/

            /*$('#idea-txt-1').magicSuggest({
                // selectionPosition: 'right',
                selectionCls: 'selectedx',
                renderer: function(city){
                    return '<div>' +
                            '<div style="font-family: Arial; font-weight: bold">' + city.name + '</div>' +
                            '<div><b>Text</b>: ' + city.coolness + '</div>' +
                           '</div>';
                },
                minChars: 1,
                selectionStacked: true,
                data: '/ajax/autocomplete/?autocomplete=' //jsonData2
            });      */                  
 //       });
            $('#idea-txt-1').magicSuggest({
                // selectionPosition: 'right',
                selectionCls: 'selectedx',
                renderer: function(idea){
                    //console.log(idea.name)
                    return '<div>' +
                            '<div style="font-family: Arial; font-weight: bold">' + idea.name + '</div>' +
                            '<div><b>Text</b>: ' + idea.text + '</div>' +
                           '</div>';
                },
                minChars: 0,
                selectionStacked: true,
                method:'GET',
                expanded:true,
                expandOnFocus:true,
                maxDropHeight:'500px',

                name:'query',
                data: '/ajax/autocomplete/' //jsonData2
            });                  


    },

    selectionlist: function() {
        var r = ''
        $.each($('.selectedx'), function(i, j) {
            if(r!='') r += '<sep>';
            r = r + $(j).text();
        });
        return r;
    },

    explorableTags: function() {

        //$('span.label').click(function() {
        $('body').on('click','span.label',function() {
                lthis=$(this)
                    $.getJSON('/ajax/getIdeaById/', {'title':$(this).html(),'id':$(this).attr('data-id')},function(xdata) {

                        console.log($(this))
                        idea=xdata[0];
                        //$.each(xdata,function(idea) {
                            //alert(idea['title'])
                            //console.log(lthis.parentsUntil('ul').children('.entryChildren').first().children('.idealist').first().html())
                            var t='<li class="li-idea container-fluid li-idea" data-id="' + idea['id'] + '">'+
                            '              <div class="entryBody">'+
                            '                <div class="row-fluid">'+
                            '                  <div class="span1" style="text-align:center;">'+
                            '                    <div class="row">'+
                            '                      <img src="/static/arroworange.png" class="upvote" data-id="' + idea['id'] + '">'+
                            '                      <span class="numvotes">' + idea['upvotes'] +'</span>'+
                            '                    </div>'+
                            '                    <!-- <div class="row">'+
                            '                      <img src="/static/arrow.png" class="downvote" data-id="' + idea['id'] + '">'+
                            '                    </div>-->'+
                            '                  </div>'+
                            '                  <div class="span11">'+
                            '                    <div class="clearfix">'+
                            '                      <a class="li-idea-title" href="/idea/' + idea['id'] + '/">' + idea['name'] + ':&nbsp;</a>'+
                            '                      <div class="li-idea-body">'+
                            '                        <div class="li-idea-text">' + idea['text'] + '</div>'+
                            '                      </div>'+
                            '                    </div>'+
                            '                    <div class="li-idea-tags">';
                            tagsray=idea.tags.split('<sep>')
                            for(i in tagsray)
                                t+='<span class="label label-info">' + tagsray[i] + '</span>&nbsp;';


                            t+='</div>'+
                            '                  </div>'+
                            '                </div>'+
                            '              </div>'+
                            '              <div class="entryChildren">'+
                            '                <ul class="idealist">'+
                            '                  '+
                            '                </ul>'+
                            '              </div>'+
                            '            </li>'

                            //if not already present at this level
                            if(!lthis.parentsUntil('ul').children('.entryChildren').children('.idealist').children().filter('[data-id="'+idea['id']+'"]').length>0) {
                                //alert("not already there at this level")
                                lthis.parentsUntil('ul').children('.entryChildren').children('.idealist').append(t);
                            }
                            //lib('home').explorableTags();
                        //});


        //               
                    })
        //            $('.entryChildren > .idealist').append('<li>'+$(this).html()+'<li>')
                })

    }
});

lib('ideas', {
    events: function() {
        $('.li-idea .upvote, .li-idea .downvote').click(function() {
            var id = $(this).attr('data-id');
            lib('ideas').upvote(id, function(res) { $('.li-idea[data-id="' + id + '"] .numvotes').html(res.upvotes) });
        });
    },
    
    upvote: function(id, success) {
        // check not already voted
        if ($('.li-idea[data-id="' + id + '"] .numvotes').attr('voted') != 'true') {
        lib('util').post('/ajax/upvote/', {
            type: 'idea',
            id: id
        },
        success);
        $('.li-idea[data-id="' + id + '"] .numvotes').attr('voted','true');
        }
    },
    
    add: function() {
        var idea = {
            title: $('#idea-form .idea-form-title').val(),
            text: $('#idea-form .idea-form-text').val(),
            tags: lib('home').selectionlist()
        }
        
        if(idea.title == '' || idea.text == '') {
            alert('An blank idea is worth nothing. Complete the fields.');
            return;
        }
        
        // empty the values
        $('#idea-form .idea-form-title').val('');
        $('#idea-form .idea-form-text').val('');
        
        // send the idea to the server
        lib('util').post('/ajax/addidea/', idea, function(response) {
            // creates an empty template, so that the idea could be prepended without
            var li = lib('util').clone('li-idea-template');
            
            $(li).find('.li-idea-title').html(response.title + ":&nbsp;");
            $(li).find('.li-idea-text').html(response.text);
            $(li).find('.li-idea-title').attr('href', '/idea/' + response.id + '/');
            $(li).find('.numvotes').html(response.upvotes);
            $(li).attr('data-id', response.id);
            $(li).find('.upvote').attr('data-id', response.id);
            
            for(var i=0;i<response.tags.length;++i)
                $(li).find('.li-idea-tags').html($(li).find('.li-idea-tags').html() + '&nbsp;<span class="label label-info">' + response.tags[i] + '</span>');
                
            $(li).find('.upvote').click(function() {
                lib('ideas').upvote(response.id, function(res) { $('.li-idea[data-id="' + response.id + '"] .numvotes').html(res.upvotes) });
            });
            
            $('.idealist').prepend(li);
        });
    }
});

lib('suggestions', {
    init: function() {
        this.events();
    },
    
    events: function() {
        $('.li-suggestion .upvote').click(function() {
            var id = $(this).attr('data-id');
            lib('suggestions').upvote(id, function(res) { $('.li-suggestion[data-id="' + id + '"] .numvotes').html(res.upvotes) });
        });
    },
    
    upvote: function(id, success) {
        lib('util').post('/ajax/upvote/', {
            type: 'suggestion',
            id: id
        },
        success);
    },
    
    add: function() {
        var suggestion = {
            idea: window.locals.idea,
            text: $('#suggestion-form .suggestion-form-text').val()
        }
        
        if(suggestion.text == '') {
            alert('An blank idea is worth nothing. Complete the fields.');
            return;
        }
        
        // empty the values
        $('#suggestion-form .suggestion-form-text').val('');
        
        // send the idea to the server
        lib('util').post('/ajax/addsuggestion/', suggestion, function(response) {
            // creates an empty template, so that the idea could be prepended without
            var li = lib('util').clone('li-suggestion-template');
            
            $(li).find('.li-suggestion-text').html(response.text);
            $(li).find('.numvotes').html(response.upvotes);
            $(li).attr('data-id', response.id);
            $(li).find('.upvote').attr('data-id', response.id);
            
            $(li).find('.upvote').click(function() {
                lib('suggestions').upvote(response.id, function(res) { $('.li-suggestion[data-id="' + response.id + '"] .numvotes').html(res.upvotes) });
            });
            
            $('.suggestionlist').prepend(li);
        });
    }
});
