$(document).ready(function(){
    var update_panels=function(data){
        for(var panel in data){     
            $("#"+panel).html(data[panel]);
        }
    };
    // for each menu item, bind a click event
    // note: each menu item will have an id that starts with "menu_"
    $("a[id^=menu_]").each(function(){
        $("#" + $(this)[0].id).live('click',function(){
          $.getJSON(
            $SCRIPT_ROOT + '/_menu',
            {id: $(this)[0].id },
            function(data){update_panels(data);}
          );
          return false;
        });
    });
});
