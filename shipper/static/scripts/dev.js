(function( window ) {
  "use strict";
  var document = window.document,
      fieldValueMap = {
            "sender_name"       : "George Costanza"
          , "sender_company"    : "Vandelay Industries"
          , "sender_address1"   : "1 E 161st St."
          , "sender_address2"   : ""
          , "sender_city"       : "Bronx"
          , "sender_state"      : "NY"
          , "sender_zip_code"   : "10451"
          , "receiver_name"     : "Danny Tanner"
          , "receiver_company"  : ""
          , "receiver_address1" : "1882 Girard Street" 
          , "receiver_address2" : ""
          , "receiver_city"     : "San Francisco"
          , "receiver_state"    : "CA"
          , "receiver_zip_code" : "94134"
          , "length" : 14
          , "width"  : 12
          , "height" : 3.5
          , "weight" : 100
      };

    Object.keys( fieldValueMap ).forEach(function( name ){

        var input = document.querySelector( "form input[name='" + name + "']" )
                        || document.querySelector( "form select[name='" + name + "']" )
            || document.querySelector( "form textarea[name='" + name + "']" );

        input && input.type !== "hidden" && ( input.value = fieldValueMap[ name ] );
    });

})( window );