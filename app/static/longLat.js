
const startingLoc = [0,0];
//CONSTRUCT MAP --
const layer01 = new ol.layer.Tile({ //holds map images
    source: new ol.source.OSM() //MAP IMAGES SOURCE
});

const view01 = new ol.View({ //contains data on starting view
    center: ol.proj.fromLonLat(startingLoc),
    zoom: 0
});

const map = new ol.Map({ //creates map
    target: document.getElementById('map'),
    layers: [layer01],
    view: view01,
});

//CONSTRUCT OVERLAY
//assign variables to HTML divs
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');

const overlay = new ol.Overlay({ //create overlay
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
});
map.addOverlay(overlay);

//CLICK LISTENER
closer.onclick = function () { //creates a button to close popup
    overlay.setPosition(undefined);
    closer.blur();
    return false;
};

map.on('singleclick', function (event) { //create popup on click
        let coordinates = event.coordinate;
        overlay.setPosition(coordinates); //draw popup at coords of marker

        let coord = ol.proj.transform(event.coordinate, 'EPSG:3857', 'EPSG:4326'); //grab location data
        content.innerHTML = '<p>You clicked here:</p><code>' + coord +
      '</code>';

        fetch('/postLoc')
});

