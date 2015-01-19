/*!
 * Searchable Map Template with Google Fusion Tables
 * http://derekeder.com/searchable_map_template/
 *
 * Copyright 2012, Derek Eder
 * Licensed under the MIT license.
 * https://github.com/derekeder/FusionTable-Map-Template/wiki/License
 *
 * Date: 12/10/2012
 *
 */

// Enable the visual refresh
google.maps.visualRefresh = true;

var MapsLib = MapsLib || {};
var MapsLib = {

  //Setup section - put your Fusion Table details here
  //Using the v1 Fusion Tables API. See https://developers.google.com/fusiontables/docs/v1/migration_guide for more info

  //the encrypted Table ID of your Fusion Table (found under File => About)
  //NOTE: numeric IDs will be deprecated soon
  fusionTableId:      "1Fz3AERVhTUh0FcluxTIF2aoyJHgAeuXd2VOejrqr",

  //*New Fusion Tables Requirement* API key. found at https://code.google.com/apis/console/
  //*Important* this key is for demonstration purposes. please register your own.
  googleApiKey:       "AIzaSyDywhPPISz7KqH-vwR48w-lJt5rmO0BUkc",

  //name of the location column in your Fusion Table.
  //NOTE: if your location column name has spaces in it, surround it with single quotes
  //example: locationColumn:     "'my location'",
  locationColumn:     "objfcpgeoloc_p",

  map_centroid:       new google.maps.LatLng(36.879621, -119.926758), //center that your map defaults to
  locationScope:      "california",      //geographical area appended to all address searches
  recordName:         "location",       //for showing number of results
  recordNamePlural:   "locations",

  searchRadius:       805,            //in meters ~ 1/2 mile
  defaultZoom:        6,             //zoom level when map is loaded (bigger is more zoomed in)
  addrMarkerImage:    'images/blue-pushpin.png',
  currentPinpoint:    null,

  initialize: function() {

    $( "#result_count" ).html("");

    geocoder = new google.maps.Geocoder();
    var myOptions = {
      zoom: MapsLib.defaultZoom,
      center: MapsLib.map_centroid,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map($("#map_canvas")[0],myOptions);

    var polyOptions = {
      strokeColor: '#000000',
      strokeOpacity: 1.0,
      strokeWeight: 3
    }

    var markers = [];

    // if (markers.length == 0) {
    //   $( "#view_mode_shape" ).hide();
    // };

    poly = new google.maps.Polyline(polyOptions);
    poly.setMap(map);
    srchbtn = document.querySelector("#search-shape");
    google.maps.event.addListener(map, 'click', function(event) {
      var path = poly.getPath();
      path.push(event.latLng);
      markers.push(new google.maps.Marker({
        position: event.latLng,
        title: '#' + path.getLength(),
        icon: 'http://www.google.com/intl/en_us/mapfiles/ms/micons/blue-dot.png',
        map: map
      }));
    });

    srchbtn.addEventListener("click", function(e) {
      var path = poly.getPath();
      if(path.getLength() == 4) {
        path.push(markers[0].getPosition());
        MapsLib.polySearch();
      }
    });

    // maintains map centerpoint for responsive design
    google.maps.event.addDomListener(map, 'idle', function() {
        MapsLib.calculateCenter();
    });

    google.maps.event.addDomListener(window, 'resize', function() {
        map.setCenter(MapsLib.map_centroid);
    });

    MapsLib.searchrecords = null;

    //reset filters
    $("#search_address").val(MapsLib.convertToPlainString($.address.parameter('address')));
    var loadRadius = MapsLib.convertToPlainString($.address.parameter('radius'));
    if (loadRadius != "") $("#search_radius").val(loadRadius);
    else $("#search_radius").val(MapsLib.searchRadius);
    $(":checkbox").prop("checked", "checked");
    $("#resultlist").hide();
    $(".alert").hide();
    $("#back-search").hide();
    console.log("initialize");
    $("#view_mode").hide();
    $("#view_mode_shape").hide();

    
    //-----custom initializers-------
    
    //-----end of custom initializers-------

    //run the default search
    MapsLib.doSearch();
  },

  polySearch: function() {
    console.log("running polysearch");
    var totalFound = 0;
    var total = [];

    for(var i=0; i<locData.length; i++) {
      ll = locData[i][0];
      t = ll.split(", ");
      var point = new google.maps.LatLng(t[0], t[1]);
      if(google.maps.geometry.poly.containsLocation(point, poly)) {
        var m = new google.maps.Marker({
          position: point,
          title: 'Location '+i,
          map: map
        });
        totalFound++;
        total.push(locData[i]);
      }
    }
    var results_shape = $("#resultlist_shape");
    results_shape.hide().empty();
    for (var row in total) {
      for (var l in n=total[row][1].split("; ")) {
        template = "\
        <div class='row-fluid item-list'>\
          <div class='span12'>\
            <strong>" + total[row][0] + "</strong>\
            <br />\
            <a>" + n[l] + "\
          </a></div>\
        </div>";
        results_shape.append(template);
      }
    }
    if (totalFound == 1)
      name = "Location";
    else
      name = "Locations";
    $( ".alert" ).show();
    $( "#view_mode_shape" ).show();
    $( "#result_count" ).html(totalFound + " " + name + " found");
  },

  doSearch: function(location) {
    console.log("running doSearch");

    MapsLib.clearSearch();
    var address = $("#search_address").val();
    MapsLib.searchRadius = $("#search_radius").val();

    var whereClause = MapsLib.locationColumn + " not equal to ''";

    //-----custom filters-------

    //-------end of custom filters--------

    if (address != "") {
      if (address.toLowerCase().indexOf(MapsLib.locationScope) == -1)
        address = address + " " + MapsLib.locationScope;

      geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
          MapsLib.currentPinpoint = results[0].geometry.location;

          $.address.parameter('address', encodeURIComponent(address));
          $.address.parameter('radius', encodeURIComponent(MapsLib.searchRadius));
          map.setCenter(MapsLib.currentPinpoint);
          
          // set zoom level based on search radius
          if (MapsLib.searchRadius      >= 1610000) map.setZoom(04); // 1,000 miles
          else if (MapsLib.searchRadius >= 805000)  map.setZoom(05); // 500 miles
          else if (MapsLib.searchRadius >= 402500)  map.setZoom(06); // 250 miles
          else if (MapsLib.searchRadius >= 161000)  map.setZoom(07); // 100 miles
          else if (MapsLib.searchRadius >= 80500)   map.setZoom(08); // 50 miles
          else if (MapsLib.searchRadius >= 40250)   map.setZoom(09); // 25 miles
          else if (MapsLib.searchRadius >= 16100)   map.setZoom(11); // 10 miles
          else if (MapsLib.searchRadius >= 8050)    map.setZoom(12); // 5 miles
          else if (MapsLib.searchRadius >= 3220)    map.setZoom(13); // 2 miles
          else if (MapsLib.searchRadius >= 1610)    map.setZoom(14); // 1 mile
          else if (MapsLib.searchRadius >= 805)     map.setZoom(15); // 1/2 mile
          else if (MapsLib.searchRadius >= 400)     map.setZoom(16); // 1/4 mile
          else                                      map.setZoom(17);

          MapsLib.addrMarker = new google.maps.Marker({
            position: MapsLib.currentPinpoint,
            map: map,
            icon: MapsLib.addrMarkerImage,
            animation: google.maps.Animation.DROP,
            title:address
          });

          whereClause += " AND ST_INTERSECTS(" + MapsLib.locationColumn + ", CIRCLE(LATLNG" + MapsLib.currentPinpoint.toString() + "," + MapsLib.searchRadius + "))";

          MapsLib.drawSearchRadiusCircle(MapsLib.currentPinpoint);
          MapsLib.submitSearch(whereClause, map, MapsLib.currentPinpoint);
        }
        else {
          alert("We could not find your address: " + status);
        }
      });
    }
    else { //search without geocoding callback
      MapsLib.submitSearch(whereClause, map);
    }
  },

  submitSearch: function(whereClause, map, location) {
    //get using all filters
    //NOTE: styleId and templateId are recently added attributes to load custom marker styles and info windows
    //you can find your Ids inside the link generated by the 'Publish' option in Fusion Tables
    //for more details, see https://developers.google.com/fusiontables/docs/v1/using#WorkingStyles

    MapsLib.searchrecords = new google.maps.FusionTablesLayer({
      query: {
        from:   MapsLib.fusionTableId,
        select: MapsLib.locationColumn,
        where:  whereClause
      },
      styleId: 2,
      templateId: 2
    });
    MapsLib.searchrecords.setMap(map);
    MapsLib.getCount(whereClause);
    MapsLib.getList(whereClause);
  },

  clearSearch: function() {
    if (MapsLib.searchrecords != null)
      MapsLib.searchrecords.setMap(null);
    if (MapsLib.addrMarker != null)
      MapsLib.addrMarker.setMap(null);
    if (MapsLib.searchRadiusCircle != null)
      MapsLib.searchRadiusCircle.setMap(null);
  },

  findMe: function() {
    // Try W3C Geolocation (Preferred)
    var foundLocation;

    if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        foundLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
        MapsLib.addrFromLatLng(foundLocation);
      }, null);
    }
    else {
      alert("Sorry, we could not find your location.");
    }
  },

  addrFromLatLng: function(latLngPoint) {
    geocoder.geocode({'latLng': latLngPoint}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[1]) {
          $('#search_address').val(results[1].formatted_address);
          $('.hint').focus();
          MapsLib.doSearch();
        }
      } else {
        alert("Geocoder failed due to: " + status);
      }
    });
  },

  drawSearchRadiusCircle: function(point) {
      var circleOptions = {
        strokeColor: "#4b58a6",
        strokeOpacity: 0.3,
        strokeWeight: 1,
        fillColor: "#4b58a6",
        fillOpacity: 0.05,
        map: map,
        center: point,
        clickable: false,
        zIndex: -1,
        radius: parseInt(MapsLib.searchRadius)
      };
      MapsLib.searchRadiusCircle = new google.maps.Circle(circleOptions);
  },

  query: function(selectColumns, whereClause, groupBy, orderBy, callback) {
    var queryStr = [];
    queryStr.push("SELECT " + selectColumns);
    queryStr.push(" FROM " + MapsLib.fusionTableId);
    
    // where, group and order clauses are optional
    if (whereClause != "" && whereClause != null)
      queryStr.push(" WHERE " + whereClause);

    if (groupBy != "" && groupBy != null)
      queryStr.push(" GROUP BY " + groupBy);

     if (orderBy != "" && orderBy != null)
      queryStr.push(" ORDER BY " + orderBy);

    var sql = encodeURIComponent(queryStr.join(" "));
    $.ajax({url: "https://www.googleapis.com/fusiontables/v1/query?sql="+sql+"&callback="+callback+"&key="+MapsLib.googleApiKey, dataType: "jsonp"});
  },

  handleError: function(json) {
    if (json["error"] != undefined) {
      var error = json["error"]["errors"]
      console.log("Error in Fusion Table call!");
      for (var row in error) {
        console.log(" Domain: " + error[row]["domain"]);
        console.log(" Reason: " + error[row]["reason"]);
        console.log(" Message: " + error[row]["message"]);
      }
    }
  },

  getCount: function(whereClause) {
    var selectColumns = "Count()";
    MapsLib.query(selectColumns, whereClause, "", "", "MapsLib.displaySearchCount");
  },

  displaySearchCount: function(json) {
    console.log("running displaySearchCount");

    var address = $("#search_address").val();

    MapsLib.handleError(json);
    var numRows = 0;
    if (json["rows"] != null)
      numRows = json["rows"][0];

    var name = MapsLib.recordNamePlural;
    if (numRows == 1)
    name = MapsLib.recordName;
    $( "#result_box" ).fadeOut(function() {
        $( "#result_count" ).html(MapsLib.addCommas(numRows) + " " + name + " found");
      });
    $( "#result_box" ).fadeIn();
    if (numRows != 0 && address != "") {
      $( "#view_mode" ).fadeIn();
    }
  },

  getList: function(whereClause) {
    var selectColumns = "objfcpgeoloc_p, objassoccult_ss ";
    MapsLib.query(selectColumns, whereClause, "", "", "MapsLib.displayList");
  },

  displayList: function(json) {
    MapsLib.handleError(json);
    var data = json["rows"];
    locData = data;
    var template = "";

    var results = $("#resultlist");
    results.hide().empty(); //hide the existing list and empty it out first

    if (data == null) {
      //clear results list
      results.append("<li><span class='lead'>No results found</span></li>");
    }
    else {
      for (var row in data) {
        for (var l in n=data[row][1].split("; ")) {
          template = "\
          <div class='row item-list'>\
            <div class='col-md-12'>\
              <strong>" + data[row][0] + "</strong>\
              <br />\
              <a style='cursor: pointer' href='/artifacts.html/" + n[l] + "'>" + n[l] + "\
            </a></div>\
          </div>";
          results.append(template);
        }
      };
      // $( "#view_mode_shape" ).show();
    };
  },

  addCommas: function(nStr) {
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
      x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
  },

  // maintains map centerpoint for responsive design
  calculateCenter: function() {
    center = map.getCenter();
  },

  //converts a slug or query string in to readable text
  convertToPlainString: function(text) {
    if (text == undefined) return '';
    return decodeURIComponent(text);
  }
  
  //-----custom functions-------
  // NOTE: if you add custom functions, make sure to append each one with a comma, except for the last one.
  // This also applies to the convertToPlainString function above
  
  //-----end of custom functions-------
}
